from pyspark.sql import SparkSession

spark = SparkSession.builder.master('local').appName('word count').config('spark.some.config.option','some-value').enableHiveSupport().getOrCreate()

spark.sql('use toutiao')
basic_content = spark.sql("select a.article_id, a.channel_id, a.title, b.content from news_article_basic a inner join news_article_content b on a.article_id=b.article_id where a.article_id=116636")

print(basic_content)
