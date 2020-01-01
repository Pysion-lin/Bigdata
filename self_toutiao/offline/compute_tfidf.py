import os
import sys
BASE_DIR = os.path.dirname(os.getcwd())
sys.path.insert(0,os.path.join(BASE_DIR))
PYSPARK_PYTHON = '/miniconda2/envs/reco_sys/bin/python'

os.environ['PYSPARK_PYTHON'] = PYSPARK_PYTHON
os.environ['PYSPARK_DRIVER_PYTHON'] = PYSPARK_PYTHON

from config import SparkSessionBases
class KeywordsToTfidf(SparkSessionBases):
    SPARK_APP_NAME = 'keywordByTFIDF'
    SPARK_URL = 'local'
    ENABLE_HIVE_SUPPORT = True

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

article_dataframe = ktt.spark.sql('select * from article_data limit 1')
words_df = article_dataframe.rdd.mapPartitions(segmentation).toDF(['article_id','channel_id','words'])
print(words_df)



















