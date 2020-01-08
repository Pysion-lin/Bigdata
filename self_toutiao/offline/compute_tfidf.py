import os
import sys
from pyspark.ml.feature import CountVectorizer,IDF
from pyspark.ml.feature import CountVectorizerModel

BASE_DIR = os.path.dirname(os.getcwd())
sys.path.insert(0,os.path.join(BASE_DIR))
PYSPARK_PYTHON = '/miniconda2/envs/reco_sys/bin/python'

os.environ['PYSPARK_PYTHON'] = PYSPARK_PYTHON
os.environ['PYSPARK_DRIVER_PYTHON'] = PYSPARK_PYTHON

from config import SparkSessionBases
class KeywordsToTfidf(SparkSessionBases):
    SPARK_APP_NAME = 'keywordByTFIDF'
    SPARK_URL = 'spark://master:7077'
    ENABLE_HIVE_SUPPORT = True
    SPARK_EXECUTOR_MEMORY = '2g'
    SPARK_EXECUTOR_CORES = 4
    SPARK_EXECUTOR_INSTANCES = 8

    def __init__(self):
        self.spark = self._create_spark_session()

ktt = KeywordsToTfidf()
ktt.spark.sql('use article')


def segmentation(partition):
    import os
    import re
    import jieba
    import jieba.analyse
    import jieba.posseg
    import jieba.posseg as pseg
    import codecs

    abspath = '/root/words'
    userDict_path = os.path.join(abspath,'ITKeywords.txt')
    jieba.load_userdict(userDict_path)

    stopwords_path = os.path.join(abspath,"stopwords.txt")
    def get_stopwords_list():
        stopwords_list = [i.strip() for i  in codecs.open(stopwords_path).readline()]
        return stopwords_list
    stopwords_list = get_stopwords_list()

    def cut_sentence(sentence):
        seg_list = pseg.lcut(sentence)
        seg_list = [i for i in seg_list if i.flag not in stopwords_list]
        filtered_word_list = []
        for seg in seg_list:
            if len(seg.word) <= 1:
                continue
            elif seg.flag == 'eng':
                if len(seg.word) <= 2:
                    continue
                else:
                    filtered_word_list.append(seg.word)
            elif seg.flag.startswith('n'):
                filtered_word_list.append(seg.word)
            elif seg.flag in ['x','eng']:
                filtered_word_list.append(seg.word)
        return filtered_word_list

    for row in partition:
        sentence = re.sub("<.*?>","",row.sentence)
        words = cut_sentence(sentence)
        yield row.article_id,row.channel_id,words

article_dataframe = ktt.spark.sql('select * from article_data')
words_df = article_dataframe.rdd.mapPartitions(segmentation).toDF(['article_id','channel_id','words'])
# print(words_df.collect())
try:
    print('正在判断CV模型是否存在')
    ktt.textFile('hdfs://master:9000/headlines/model/CV.model')
    # print(cv_model)
    print('模型存在')
except Exception as e:
    print(e)
    print('不存在模型，启动训练')
    cv = CountVectorizer(inputCol='words', outputCol='countFeatures', vocabSize=200 * 10000, minDF=1.0)
    # cv_model = cv.fit(words_df)
    # cv_model.write().overwrite().save('hdfs://master:9000/headlines/model/CV.model')
finally:
    print('读取模型：。。。。')
    cv_model= CountVectorizerModel.load('hdfs://master:9000/headlines/model/CV.model')
    print('将模型的词频统计转化为词的向量')
    cv_result = cv_model.transform(words_df)
    print('利用计算的词向量训练向量模型并保存')
    idf = IDF(inputCol='countFeatures',outputCol='idfFeatures')
    idfmode = idf.fit(cv_result)
    idfmode.write().overwrite().save('hdfs://master:9000/headlines/model/IDF.model')
    print('IDF模型训练并保存成功')


print('查看cv_model模型效果：')
print(cv_model.vocabulary)
print('查看IDF模型效果：')
print(idfmode.idf.toArray[:20])










