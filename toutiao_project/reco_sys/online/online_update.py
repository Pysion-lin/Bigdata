import os
import sys
BASE_DIR = os.path.dirname(os.getcwd())
sys.path.insert(0, os.path.join(BASE_DIR))

# 添加环境变量
os.environ['JAVA_HOME'] = '/root/bigdata/jdk'
os.environ['SPARK_HOME'] = '/root/bigdata/spark'
os.environ['HADOOP_HOME'] = '/root/bigdata/hadoop'
os.environ['PYSPARK_PYTHON'] = '/miniconda2/envs/reco_sys/bin/python'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/miniconda2/envs/reco_sys/bin/python'
os.environ["PYSPARK_SUBMIT_ARGS"] = "--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.2 pyspark-shell"

from online import stream_c, SIMILAR_DS, HOT_DS, NEW_ARTICLE_DS, pool
from datetime import datetime
import redis
import json
import time
from settings import logging as lg
from settings.default import DefaultConfig
import logging

logger = logging.getLogger('online')


class OnlineRecall(object):
    """在线处理计算平台
    """
    def __init__(self):
        self.client = redis.StrictRedis(host=DefaultConfig.REDIS_HOST,
                                        port=DefaultConfig.REDIS_PORT,
                                        db=10)
        self.k = 10

    def _update_hot_redis(self):
        """更新热门文章  click-trace
        :return:
        """
        client = self.client

        def updateHotArt(rdd):
            for row in rdd.collect():
                logger.info("{}, INFO: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), row))
                # 如果是曝光参数，和阅读时长选择过滤
                if row['param']['action'] == 'exposure' or row['param']['action'] == 'read':
                    pass
                else:
                    # 解析每条行为日志，然后进行分析保存点击，喜欢，分享次数，这里所有行为都自增1
                    client.zincrby("ch:{}:hot".format(row['channelId']), 1, row['param']['articleId'])

        HOT_DS.map(lambda x: json.loads(x[1])).foreachRDD(updateHotArt)

        return None

    def _update_new_redis(self):
        """更新频道新文章 new-article
        :return:
        """
        client = self.client

        def computeFunction(rdd):
            for row in rdd.collect():
                channel_id, article_id = row.split(',')
                logger.info("{}, INFO: get kafka new_article each data:channel_id{}, article_id{}".format(
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'), channel_id, article_id))
                client.zadd("ch:{}:new".format(channel_id), {article_id: time.time()})

        NEW_ARTICLE_DS.map(lambda x: x[1]).foreachRDD(computeFunction)

        return None

    def _update_online_cb(self):
        """
        通过点击行为更新用户的cb召回表中的online召回结果
        :return:
        """
        def foreachFunc(rdd):

            for data in rdd.collect():
                logger.info(
                    "{}, INFO: rdd filter".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                # 判断日志行为类型，只处理点击流日志
                if data["param"]["action"] in ["click", "collect", "share"]:
                    # print(data)
                    with pool.connection() as conn:
                        try:
                            # 相似文章表
                            sim_table = conn.table("article_similar")

                            # 根据用户点击流日志涉及文章找出与之最相似文章(基于内容的相似)，选取TOP-k相似的作为召回推荐结果
                            _dic = sim_table.row(str(data["param"]["articleId"]).encode(), columns=[b"similar"])
                            _srt = sorted(_dic.items(), key=lambda obj: obj[1], reverse=True)  # 按相似度排序
                            if _srt:

                                topKSimIds = [int(i[0].split(b":")[1]) for i in _srt[:self.k]]

                                # 根据历史推荐集过滤，已经给用户推荐过的文章
                                history_table = conn.table("history_recall")

                                _history_data = history_table.cells(
                                    b"reco:his:%s" % data["param"]["userId"].encode(),
                                    b"channel:%d" % data["channelId"]
                                )
                                # print("_history_data: ", _history_data)

                                history = []
                                if len(data) >= 2:
                                    for l in data[:-1]:
                                        history.extend(eval(l))
                                else:
                                    history = []

                                # 根据历史召回记录，过滤召回结果
                                recall_list = list(set(topKSimIds) - set(history))

                                # print("recall_list: ", recall_list)
                                logger.info("{}, INFO: store user:{} cb_recall data".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), data["param"]["userId"]))
                                if recall_list:
                                    # 如果有推荐结果集，那么将数据添加到cb_recall表中，同时记录到历史记录表中
                                    logger.info(
                                        "{}, INFO: get online-recall data".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                                    recall_table = conn.table("cb_recall")

                                    recall_table.put(
                                        b"recall:user:%s" % data["param"]["userId"].encode(),
                                        {b"online:%d" % data["channelId"]: str(recall_list).encode()}
                                    )

                                    history_table.put(
                                        b"reco:his:%s" % data["param"]["userId"].encode(),
                                        {b"channel:%d" % data["channelId"]: str(recall_list).encode()}
                                    )
                        except Exception as e:
                            logger.info("{}, WARN: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), e))
                        finally:
                            conn.close()

        SIMILAR_DS.map(lambda x: json.loads(x[1])).foreachRDD(foreachFunc)

        return None

if __name__ == '__main__':
    # 启动日志配置
    lg.create_logger()
    op = OnlineRecall()
    op._update_online_cb()
    op._update_hot_redis()
    op._update_new_redis()
    stream_c.start()
    # 使用 ctrl+c 可以退出服务
    _ONE_DAY_IN_SECONDS = 60 * 60 * 24
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

