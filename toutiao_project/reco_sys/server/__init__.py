import happybase
import redis
from settings.default import DefaultConfig

# hbase连接池
pool = happybase.ConnectionPool(size=10, host='192.168.19.137', port=9090)

# redis连接
redis_client = redis.StrictRedis(host=DefaultConfig.REDIS_HOST,
                                 port=DefaultConfig.REDIS_PORT,
                                 db=10,
                                 decode_responses=True)

# 实时推荐的二级缓存数据缓存在8号当中
cache_client = redis.StrictRedis(host=DefaultConfig.REDIS_HOST,
                                 port=DefaultConfig.REDIS_PORT,
                                 db=8,
                                 decode_responses=True)

from pyspark import SparkConf
from pyspark.sql import SparkSession
import os

# 添加环境变量

os.environ['JAVA_HOME'] = '/root/bigdata/jdk'
os.environ['SPARK_HOME'] = '/root/bigdata/spark'
os.environ['HADOOP_HOME'] = '/root/bigdata/hadoop'
os.environ['PYSPARK_PYTHON'] = '/miniconda2/envs/reco_sys/bin/python'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/miniconda2/envs/reco_sys/bin/python'

# spark配置
conf = SparkConf()
conf.setAll(DefaultConfig.SPARK_GRPC_CONFIG)

SORT_SPARK = SparkSession.builder.config(conf=conf).getOrCreate()

