from pyspark import SparkConf
from pyspark.sql import SparkSession
import os
class SparkSessionBases(object):
 
	SPARK_APP_NAME = None 
	SPARK_URL = 'yarn'
	SPARK_EXECUTOR_MEMORY = '2g' 
	SPARK_EXECUTOR_CORES = 2
	SPARK_EXECUTOR_INSTANCES = 2
	ENABLE_HIVE_SUPPORT = False

	def _create_spark_session(self):
		conf = SparkConf()
		config = (
			('spark.app.name',self.SPARK_APP_NAME),
			('spark.executor.memory',self.SPARK_EXECUTOR_MEMORY),
			('spark.master',self.SPARK_URL),
			('spark.executor.cores',self.SPARK_EXECUTOR_CORES),
			('spark.executor.instances',self.SPARK_EXECUTOR_INSTANCES),
			)
		conf.setAll(config)
		if self.ENABLE_HIVE_SUPPORT:
			return SparkSession.builder.config(conf=conf).enableHiveSupport().getOrCreate()
		else:
			return SparkSession.builder.config(conf=conf).getOrCreate()


   
