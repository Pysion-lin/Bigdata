import os
import sys
import gc
import pyspark.sql.functions as F


BASE_DIR = os.path.dirname(os.getcwd())
sys.path.insert(0,os.path.join(BASE_DIR))
PYSPARK_PYTHON = '/miniconda2/envs/reco_sys/bin/python'

os.environ['PYSPARK_PYTHON'] = PYSPARK_PYTHON
os.environ['PYSPARK_DRIVER_PYTHON'] = PYSPARK_PYTHON

from config import SparkSessionBases
class OriginArticleData(SparkSessionBases):
    SPARK_APP_NAME = 'mergeArticle'
    SPARK_URL = 'local'
    ENABLE_HIVE_SUPPORT = True
    def __init__(self):
        self.spark = self._create_spark_session()

oa = OriginArticleData()
oa.spark.sql('use toutiao')
basic_content = oa.spark.sql('select a.article_id,a.channel_id,a.title,b.content from news_article_basic  a '
                             'inner join news_article_content b on a.article_id=b.article_id where a.article_id=116636')


basic_content.registerTempTable("temparticle")
channel_basic_content = oa.spark.sql(
  "select t.*, n.channel_name from temparticle t left join news_channel n on t.channel_id=n.channel_id")

# 利用concat_ws方法，将多列数据合并为一个长文本内容（频道，标题以及内容合并）
oa.spark.sql("use article")
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