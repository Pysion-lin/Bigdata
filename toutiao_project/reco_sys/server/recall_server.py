import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR))

from server import redis_client
from server import pool
import logging
from datetime import datetime
from server.utils import HBaseUtils

logger = logging.getLogger('recommend')


class ReadRecall(object):
    """读取召回集的结果
    """
    def __init__(self):
        self.client = redis_client
        self.hbu = HBaseUtils(pool)
        self.hot_num = 10

    def read_hbase_recall_data(self, table_name, key_format, column_format):
        """
        读取用户指定召回表中的召回结果
        :param table_name: 召回表名字
        :param key_format: 键，用户
        :param column_format: 列族，哪个频道
        :return:
        """
        recall_list = []
        # 需要异常处理
        try:
            # 读取这个频道所有版本数据，合并到一起
            data = self.hbu.get_table_cells(table_name, key_format, column_format)

            for _ in data:
                recall_list = list(set(recall_list).union(set(eval(_))))

            # 删除召回结果, 为了测试我们暂时不删除数据，否则还得创造测试数据
            # self.hbu.get_table_delete(table_name, key_format, column_format)

        except Exception as e:
            logger.warning("{} WARN read {} recall exception:{}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                        table_name, e))
        return recall_list

    def read_redis_new_article(self, channel_id):
        """
        读取新 文章的redis
        :param channel_id: 具体频道的new article
        :return:
        """

        _key = "ch:{}:new".format(channel_id)
        try:
            res = self.client.zrevrange(_key, 0, -1)
            logger.info("{} INFO read channel_id:{} new article:{}".
                        format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), channel_id, res))
        except Exception as e:
            res = []
            logger.info("{} WARN exception:{}".
                        format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), e))

        # res里面的文章ID是字符串---->int
        return list(map(int, res))

    def read_redis_hot_article(self, channel_id):
        """
        读取新闻章召回结果
        :param channel_id: 提供频道
        :return:
        """
        logger.warning("{} WARN read channel {} redis hot article".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                          channel_id))
        _key = "ch:{}:hot".format(channel_id)
        try:
            res = self.client.zrevrange(_key, 0, -1)

        except Exception as e:
            logger.warning(
                "{} WARN read new article exception:{}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), e))
            res = []

        # 做一个数量处理取出TOPK
        res = list(map(int, res))
        if len(res) > self.hot_num:
            res = res[:self.hot_num]
        return res

    def read_hbase_article_similar(self, table_name, key_format, article_num):
        """获取文章相似结果
        :param article_id: 文章id
        :param article_num: 文章数量
        :return:
        """
        # 第一种表结构方式测试：
        # create 'article_similar', 'similar'
        # put 'article_similar', '1', 'similar:1', 0.2
        # put 'article_similar', '1', 'similar:2', 0.34
        try:
            _dic = self.hbu.get_table_row(table_name, key_format)

            res = []
            _srt = sorted(_dic.items(), key=lambda obj: obj[1], reverse=True)
            if len(_srt) > article_num:
                _srt = _srt[:article_num]
            for _ in _srt:
                res.append(int(_[0].decode().split(':')[1]))
        except Exception as e:
            logger.error(
                "{} ERROR read similar article exception: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), e))
            res = []
        return res


if __name__ == '__main__':
    rr = ReadRecall()
    # print(rr.read_hbase_recall_data('cb_recall', b'recall:user:2', b'als:18'))
    # print(rr.read_redis_new_article(18))
    # print(rr.read_redis_hot_article(18))
