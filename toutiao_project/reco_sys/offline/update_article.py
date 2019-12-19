import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR))
from offline import SparkSessionBase
from datetime import datetime
from datetime import timedelta
# from setting.default import CHANNEL_INFO
from settings.default import CHANNEL_INFO
import pyspark.sql.functions as F
import pyspark
import gc
import logging

logger = logging.getLogger("offline")

# 添加环境变量
os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['JAVA_HOME'] = '/root/bigdata/jdk'
os.environ['SPARK_HOME'] = '/root/bigdata/spark'
os.environ['HADOOP_HOME'] = '/root/bigdata/hadoop'
os.environ['PYSPARK_PYTHON'] = '/miniconda2/envs/reco_sys/bin/python'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/miniconda2/envs/reco_sys/bin/python'

# 分词
def segmentation(partition):
    import os
    import re

    import jieba
    import jieba.analyse
    import jieba.posseg as pseg
    import codecs

    abspath = "/root/words"

    # 结巴加载用户词典
    userDict_path = os.path.join(abspath, "ITKeywords.txt")
    jieba.load_userdict(userDict_path)

    # 停用词文本
    stopwords_path = os.path.join(abspath, "stopwords.txt")

    def get_stopwords_list():
        """返回stopwords列表"""
        stopwords_list = [i.strip()
                          for i in codecs.open(stopwords_path).readlines()]
        return stopwords_list

    # 所有的停用词列表
    stopwords_list = get_stopwords_list()

    # 分词
    def cut_sentence(sentence):
        """对切割之后的词语进行过滤，去除停用词，保留名词，英文和自定义词库中的词，长度大于2的词"""
        # print(sentence,"*"*100)
        # eg:[pair('今天', 't'), pair('有', 'd'), pair('雾', 'n'), pair('霾', 'g')]
        seg_list = pseg.lcut(sentence)
        seg_list = [i for i in seg_list if i.flag not in stopwords_list]
        filtered_words_list = []
        for seg in seg_list:
            # print(seg)
            if len(seg.word) <= 1:
                continue
            elif seg.flag == "eng":
                if len(seg.word) <= 2:
                    continue
                else:
                    filtered_words_list.append(seg.word)
            elif seg.flag.startswith("n"):
                filtered_words_list.append(seg.word)
            elif seg.flag in ["x", "eng"]:  # 是自定一个词语或者是英文单词
                filtered_words_list.append(seg.word)
        return filtered_words_list

    for row in partition:
        sentence = re.sub("<.*?>", "", row.sentence)    # 替换掉标签数据
        words = cut_sentence(sentence)
        yield row.article_id, row.channel_id, words


# 分词
def textrank(partition):
    import os

    import jieba
    import jieba.analyse
    import jieba.posseg as pseg
    import codecs

    abspath = "/root/words"

    # 结巴加载用户词典
    userDict_path = os.path.join(abspath, "ITKeywords.txt")
    jieba.load_userdict(userDict_path)

    # 停用词文本
    stopwords_path = os.path.join(abspath, "stopwords.txt")

    def get_stopwords_list():
        """返回stopwords列表"""
        stopwords_list = [i.strip()
                          for i in codecs.open(stopwords_path).readlines()]
        return stopwords_list

    # 所有的停用词列表
    stopwords_list = get_stopwords_list()

    class TextRank(jieba.analyse.TextRank):
        def __init__(self, window=20, word_min_len=2):
            super(TextRank, self).__init__()
            self.span = window  # 窗口大小
            self.word_min_len = word_min_len  # 单词的最小长度
            # 要保留的词性，根据jieba github ，具体参见https://github.com/baidu/lac
            self.pos_filt = frozenset(
                ('n', 'x', 'eng', 'f', 's', 't', 'nr', 'ns', 'nt', "nw", "nz", "PER", "LOC", "ORG"))

        def pairfilter(self, wp):
            """过滤条件，返回True或者False"""

            if wp.flag == "eng":
                if len(wp.word) <= 2:
                    return False

            if wp.flag in self.pos_filt and len(wp.word.strip()) >= self.word_min_len \
                    and wp.word.lower() not in stopwords_list:
                return True

    textrank_model = TextRank(window=5, word_min_len=2)
    allowPOS = ('n', "x", 'eng', 'nr', 'ns', 'nt', "nw", "nz", "c")

    for row in partition:
        tags = textrank_model.textrank(row.sentence, topK=20, withWeight=True, allowPOS=allowPOS, withFlag=False)
        for tag in tags:
            yield row.article_id, row.channel_id, tag[0], tag[1]


class UpdateArticle(SparkSessionBase):
    """
    更新文章画像
    """
    SPARK_APP_NAME = "updateArticle"
    ENABLE_HIVE_SUPPORT = True

    SPARK_EXECUTOR_MEMORY = "2g"

    def __init__(self):
        self.spark = self._create_spark_session()

        self.cv_path = "hdfs://hadoop-master:9000/headlines/models/countVectorizerOfArticleWords.model"
        self.idf_path = "hdfs://hadoop-master:9000/headlines/models/IDFOfArticleWords.model"

    def get_cv_model(self):
        # 词语与词频统计
        from pyspark.ml.feature import CountVectorizerModel
        cv_model = CountVectorizerModel.load(self.cv_path)
        return cv_model

    def get_idf_model(self):
        from pyspark.ml.feature import IDFModel
        idf_model = IDFModel.load(self.idf_path)
        return idf_model

    @staticmethod
    def compute_keywords_tfidf_topk(words_df, cv_model, idf_model):
        """保存tfidf值高的20个关键词
        :param spark:
        :param words_df:
        :return:
        """
        cv_result = cv_model.transform(words_df)
        tfidf_result = idf_model.transform(cv_result)
        # print("transform compelete")

        # 取TOP-N的TFIDF值高的结果
        def func(partition):
            TOPK = 20
            for row in partition:
                _ = list(zip(row.idfFeatures.indices, row.idfFeatures.values))
                _ = sorted(_, key=lambda x: x[1], reverse=True)
                result = _[:TOPK]
                for word_index, tfidf in result:
                    yield row.article_id, row.channel_id, int(word_index), round(float(tfidf), 4)

        _keywordsByTFIDF = tfidf_result.rdd.mapPartitions(func).toDF(["article_id", "channel_id", "index", "tfidf"])

        return _keywordsByTFIDF

    def merge_article_data(self):
        """
        合并业务中增量更新的文章数据
        :return:
        """
        # 获取文章相关数据, 指定过去一个小时整点到整点的更新数据
        # 如：26日：1：00~2：00，2：00~3：00，左闭右开
        self.spark.sql("use toutiao")
        _yester = datetime.today().replace(minute=0, second=0, microsecond=0)
        start = datetime.strftime(_yester + timedelta(days=0, hours=-1, minutes=0), "%Y-%m-%d %H:%M:%S")
        end = datetime.strftime(_yester, "%Y-%m-%d %H:%M:%S")

        # 合并后保留：article_id、channel_id、channel_name、title、content
        # +----------+----------+--------------------+--------------------+
        # | article_id | channel_id | title | content |
        # +----------+----------+--------------------+--------------------+
        # | 141462 | 3 | test - 20190316 - 115123 | 今天天气不错，心情很美丽！！！ |
        basic_content = self.spark.sql(
            "select a.article_id, a.channel_id, a.title, b.content from news_article_basic a "
            "inner join news_article_content b on a.article_id=b.article_id where a.review_time >= '{}' "
            "and a.review_time < '{}' and a.status = 2".format(start, end))
        # 增加channel的名字，后面会使用
        basic_content.registerTempTable("temparticle")
        channel_basic_content = self.spark.sql(
            "select t.*, n.channel_name from temparticle t left join news_channel n on t.channel_id=n.channel_id")

        # 利用concat_ws方法，将多列数据合并为一个长文本内容（频道，标题以及内容合并）
        self.spark.sql("use article")
        sentence_df = channel_basic_content.select("article_id", "channel_id", "channel_name", "title", "content", \
                                                   F.concat_ws(
                                                       ",",
                                                       channel_basic_content.channel_name,
                                                       channel_basic_content.title,
                                                       channel_basic_content.content
                                                   ).alias("sentence")
                                                   )
        del basic_content
        del channel_basic_content
        gc.collect()

        # 打印日志
        logger.info(
            "{} INFO: completely merger article data".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        sentence_df.write.insertInto("article_data")
        return sentence_df

    def generate_article_label(self, sentence_df):
        """
        生成文章标签  tfidf, textrank
        :param sentence_df: 增量的文章内容
        :return:
        """
        # 进行分词
        words_df = sentence_df.rdd.mapPartitions(segmentation).toDF(["article_id", "channel_id", "words"])
        cv_model = self.get_cv_model()
        idf_model = self.get_idf_model()

        # 1、保存所有的词的idf的值，利用idf中的词的标签索引
        # 工具与业务隔离
        _keywordsByTFIDF = UpdateArticle.compute_keywords_tfidf_topk(words_df, cv_model, idf_model)

        keywordsIndex = self.spark.sql("select keyword, index idx from idf_keywords_values")

        keywordsByTFIDF = _keywordsByTFIDF.join(keywordsIndex, keywordsIndex.idx == _keywordsByTFIDF.index).select(
            ["article_id", "channel_id", "keyword", "tfidf"])

        keywordsByTFIDF.write.insertInto("tfidf_keywords_values")

        del cv_model
        del idf_model
        del words_df
        del _keywordsByTFIDF
        gc.collect()

        # 计算textrank
        textrank_keywords_df = sentence_df.rdd.mapPartitions(textrank).toDF(
            ["article_id", "channel_id", "keyword", "textrank"])
        textrank_keywords_df.write.insertInto("textrank_keywords_values")

        # 打印日志
        logger.info(
            "{} INFO: completely article tfidf textrank".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        return textrank_keywords_df, keywordsIndex

    def get_article_profile(self, textrank, keywordsIndex):
        """
        文章画像主题词建立
        :param idf: 所有词的idf值
        :param textrank: 每个文章的textrank值
        :return: 返回建立号增量文章画像
        """
        keywordsIndex = keywordsIndex.withColumnRenamed("keyword", "keyword1")
        result = textrank.join(keywordsIndex, textrank.keyword == keywordsIndex.keyword1)

        # 1、关键词（词，权重）
        # 计算关键词权重
        _articleKeywordsWeights = result.withColumn("weights", result.textrank * result.idf).select(
            ["article_id", "channel_id", "keyword", "weights"])

        # 合并关键词权重到字典
        _articleKeywordsWeights.registerTempTable("temptable")
        articleKeywordsWeights = self.spark.sql(
            "select article_id, min(channel_id) channel_id, collect_list(keyword) keyword_list, collect_list(weights) weights_list from temptable group by article_id")
        def _func(row):
            return row.article_id, row.channel_id, dict(zip(row.keyword_list, row.weights_list))
        articleKeywords = articleKeywordsWeights.rdd.map(_func).toDF(["article_id", "channel_id", "keywords"])

        # 2、主题词
        # 将tfidf和textrank共现的词作为主题词
        topic_sql = """
                select t.article_id article_id2, collect_set(t.keyword) topics from tfidf_keywords_values t
                inner join 
                textrank_keywords_values r
                where t.keyword=r.keyword
                group by article_id2
                """
        articleTopics = self.spark.sql(topic_sql)

        # 3、将主题词表和关键词表进行合并，插入表
        articleProfile = articleKeywords.join(articleTopics,
                                              articleKeywords.article_id == articleTopics.article_id2).select(
            ["article_id", "channel_id", "keywords", "topics"])
        articleProfile.write.insertInto("article_profile")

        # 打印日志
        logger.info(
            "{} INFO: completely article profile".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        del keywordsIndex
        del _articleKeywordsWeights
        del articleKeywords
        del articleTopics
        gc.collect()

        return articleProfile

    def compute_article_similar(self, articleProfile):
        """
        计算增量文章与历史文章的相似度 word2vec
        :return:
        """
        from pyspark.ml.feature import Word2VecModel
        from pyspark.ml.linalg import Vectors
        from pyspark.ml.feature import BucketedRandomProjectionLSH
        # 得到要更新的新文章通道类别(不采用)
        # all_channel = set(articleProfile.rdd.map(lambda x: x.channel_id).collect())
        def avg(row):
            x = 0
            for v in row.vectors:
                x += v
            #  将平均向量作为article的向量
            return row.article_id, row.channel_id, x / len(row.vectors)

        for channel_id, channel_name in CHANNEL_INFO.items():

            profile = articleProfile.filter('channel_id = {}'.format(channel_id))
            wv_model = Word2VecModel.load(
                "hdfs://hadoop-master:9000/headlines/models/channel_%d_%s.word2vec" % (channel_id, channel_name))
            vectors = wv_model.getVectors()

            # 计算向量
            profile.registerTempTable("incremental")
            articleKeywordsWeights = ua.spark.sql(
                "select article_id, channel_id, keyword, weight from incremental LATERAL VIEW explode(keywords) AS keyword, weight where channel_id=%d" % channel_id)

            articleKeywordsWeightsAndVectors = articleKeywordsWeights.join(vectors,
                                                                           vectors.word == articleKeywordsWeights.keyword,
                                                                           "inner")
            articleKeywordVectors = articleKeywordsWeightsAndVectors.rdd.map(
                lambda r: (r.article_id, r.channel_id, r.keyword, r.weight * r.vector)).toDF(
                ["article_id", "channel_id", "keyword", "weightingVector"])

            articleKeywordVectors.registerTempTable("tempTable")
            articleVector = self.spark.sql(
                "select article_id, min(channel_id) channel_id, collect_set(weightingVector) vectors from tempTable group by article_id").rdd.map(
                avg).toDF(["article_id", "channel_id", "articleVector"])

            # 写入数据库
            def toArray(row):
                return row.article_id, row.channel_id, [float(i) for i in row.articleVector.toArray()]

            articleVector = articleVector.rdd.map(toArray).toDF(['article_id', 'channel_id', 'articleVector'])
            articleVector.write.insertInto("article_vector")

            import gc
            del wv_model
            del vectors
            del articleKeywordsWeights
            del articleKeywordsWeightsAndVectors
            del articleKeywordVectors
            gc.collect()

            # 得到历史数据, 转换成固定格式使用LSH进行求相似
            train = self.spark.sql("select * from article_vector where channel_id=%d" % channel_id)

            def _array_to_vector(row):
                return row.article_id, Vectors.dense(row.articleVector)

            train = train.rdd.map(_array_to_vector).toDF(['article_id', 'articleVector'])
            test = articleVector.rdd.map(_array_to_vector).toDF(['article_id', 'articleVector'])

            brp = BucketedRandomProjectionLSH(inputCol='articleVector', outputCol='hashes', seed=12345,
                                              bucketLength=1.0)
            model = brp.fit(train)
            similar = model.approxSimilarityJoin(test, train, 2.0, distCol='EuclideanDistance')

            def save_hbase(partition):
                import happybase
                pool = happybase.ConnectionPool(size=3, host='hadoop-master')
                # article_similar article_id similar:article_id sim
                with pool.connection() as conn:
                    table = conn.table("article_similar")
                    for row in partition:
                        if row.datasetA.article_id == row.datasetB.article_id:
                            pass
                        else:
                            table.put(str(row.datasetA.article_id).encode(),
                                      {b"similar:%d" % row.datasetB.article_id: b"%0.4f" % row.EuclideanDistance})
                    conn.close()

            similar.foreachPartition(save_hbase)


if __name__ == '__main__':
    ua = UpdateArticle()
    sentence_df = ua.merge_article_data()
    if sentence_df.rdd.collect():
        rank, idf = ua.generate_article_label(sentence_df)
        articleProfile = ua.get_article_profile(rank, idf)
        ua.compute_article_similar(articleProfile)

