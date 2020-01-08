import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(BASE_DIR))

from config import SparkSessionBases
from datetime import datetime
from datetime import timedelta
import pyspark.sql.functions as F
import pyspark
import gc

class UpdateArticle(SparkSessionBases):
    SPARK_APP_NAME = 'updateArticle'
    ENABLE_HIVE_SUPPORT = True
    SPARK_EXECUTOR_MEMORY = '8g'
    SPARK_EXECUTOR_CORES = 4
    SPARK_EXECUTOR_INSTANCES = 8

    def __init__(self):
        self.spark = self._create_spark_session()
        self.cv_path = ''
        self.idf_path = ''

    def get_cv_model(self):
        from pyspark.ml.feature import CountVectorizerModel
        cv_model = CountVectorizerModel.load(self.cv_path)
        return cv_model

    def get_idf_model(self):
        from pyspark.ml.feature import IDFModel
        idf_model = IDFModel.load(self.idf_path)
        return idf_model

    @staticmethod
    def compute_keywords_tfidf_topk(words_df,cv_model,idf_model):
        cv_result = cv_model.transform(words_df)
        tfidf_result = idf_model.transform(cv_result)

        def func(partition):
            TOPK=20
            for row in partition:
                _ = list(zip(row.idfFeatures.indices,row.idfFeatures.values))
                _ = sorted(_,key=lambda x:x[1],reverse=True)
                result = _[:TOPK]
                for word_indexd,tfidf in result:
                    yield row.article_id,row.channel_id,int(word_indexd),round(float(tfidf),4)
        _keywordsByTFIDF = tfidf_result.rdd.mapPartitions(func).toDF(['article_id','channel_id','index','tfidf'])
        return _keywordsByTFIDF

    def merge_article_data(self):
        '''
        合并业务中增量更新的文章数据
        :return:
        '''
        self.spark.sql('use toutiao')
        _yester = datetime.today().replace(minute=0,second=0,microsecond=0)
        start = datetime.strftime(_yester + timedelta(days=0,hours=-1,minutes=0),'%Y-%m-%d %H:%M:%S')
        end = datetime.strftime(_yester,'%Y-%m-%d %H:%M:%S')

        basic_content = self.spark.sql('select a.article_id,a.channel_id,a.title,b.content from news_article_basic'
                                       'a inner join news_article_content b on a.article_id=b.article_id where '
                                       'a.review_time >= "{}" and a.review_time < "{}" and a.status = 2'.format(start,end))

        basic_content.registerTempTable('temparticle')
        channel_basic_content = self.spark.sql('select t.* ,n.channel_name from temparticle t left join news_channel n on'
                                               't.channel_id=n.channel_id')

        self.spark.sql('use article')
        sentence_df = channel_basic_content.select('article_id','channel_id','channel_name','title','content',
                                                   F.concat_ws(',',channel_basic_content.channel_name,channel_basic_content.title,
                                                               channel_basic_content.content).alias('sentence'))
        del basic_content
        del channel_basic_content
        gc.collect()

        sentence_df.write.insertInto('article_data')
    def generate_article_label(self,sentence_df):
        '''
        生成文章标签
        :param sentence_df:
        :return:
        '''
        words_df = sentence_df.rdd.mapPartitions(segmentation).toDF(['article_id','channel_id','words'])
        cv_mode = self.get_cv_model()
        idf_model = self.get_idf_model()
        _keywordsByTFIDF = UpdateArticle.compute_keywords_tfidf_topk(words_df,cv_mode,idf_model)
        keywordsIndex = self.spark.sql('select keyword,index idx from idf_keywords_values')
        keywordsByTFIDF = _keywordsByTFIDF.join(keywordsIndex,keywordsIndex.idx==_keywordsByTFIDF.index).\
            select(['article_id','channel_id','keyword','tfidf'])
        keywordsByTFIDF.write.insertInto('tfidf_keywords_values')

    def get_article_profile(self,textrank,keywordsIndex):
        '''
        文章画像主题词建立
        :param textrank:
        :param keywordsIndex:
        :return:
        '''
        keywordsIndex = keywordsIndex.withColumnRenamed('keyword','keyword1')
        result = textrank.join(keywordsIndex,textrank.keyword == keywordsIndex.keyword1)
        _articlekeywordWeight = result.withColumn('weight',result.textrank * result.idf).select(['article_id'
                                                                                                 ,'channel_id',
                                                                                                 'keyword',
                                                                                                 'weights'])
        _articlekeywordWeight.registerTempTable('temptable')
        articlekeywordsWeights  = self.spark.sql('select article_id,min(channel_id), channel_id,'
                                               'collect_list(keyword) keyword_list , collect_list(weights) weights_list'
                                               'from temptable group by article_id')

        def _func(row):
            return row.article_id,row.channel_id,dict(zip(row.keyword_list,row.weights_list))
        articlekeywords = articlekeywordsWeights.rdd.map(_func).toDF(['article_id','channel_id','keywords'])
        topic_sql = """select t.article_id article_id2,collect_set(t.keyword) 
        topics from tfidf_keywords_values t inner join textrank_keywords_values r where t.keyword=r.keyword group by article_id2"""
        articleTopics = self.spark.sql(topic_sql)

        articleProfile = articlekeywords.join(articleTopics,articlekeywords.article_id == articleTopics.article_id2)
        articleProfile.write.insertInto('article_profile')

        del keywordsIndex
        del _articlekeywordWeight
        del articlekeywords
        del articleTopics
        gc.collect()

        return articleProfile

if __name__ == '__main__':
    ua = UpdateArticle()
    sentence_df = ua.merge_article_data()
    if sentence_df.rdd.collect():
        rank,idf = ua.generate_article_label(sentence_df)
        articleProfile = ua.get_article_profile(rank,idf)