import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR))

from concurrent import futures
from abtest import user_reco_pb2_grpc
from abtest import user_reco_pb2
from settings.default import DefaultConfig
from server.reco_cent import RecoCenter
import grpc
import json
import time
import hashlib
from settings.default import RAParam
import settings.logging as lg


# def add_track(res, temp):
#     """
#     封装埋点参数
#     :param res: 推荐文章id列表
#     :param temp: 后台的请求参数
#     :return: 埋点参数
#         文章列表参数
#         单文章参数
#     """
#     # 添加埋点参数
#     track = {}
#
#     # 准备曝光参数
#     # 全部字符串形式提供，在hive端不会有解析问题
#     _exposure = {"action": "exposure", "userId": temp.user_id, "articleId": json.dumps(res),
#                  "algorithmCombine": temp.algo}
#
#     track['param'] = json.dumps(_exposure)
#     track['recommends'] = []
#
#     # 准备其它点击参数
#     for _id in res:
#         # 构造字典
#         _dic = {}
#         _dic['article_id'] = _id
#         _dic['param'] = {}
#
#         # 准备click参数
#         _p = {"action": "click", "userId": temp.user_id, "articleId": str(_id), "algorithmCombine": temp.algo}
#
#         _dic['param']['click'] = json.dumps(_p)
#         # 准备collect参数
#         _p["action"] = 'collect'
#         _dic['param']['collect'] = json.dumps(_p)
#         # 准备share参数
#         _p["action"] = 'share'
#         _dic['param']['share'] = json.dumps(_p)
#         # 准备detentionTime参数
#         _p["action"] = 'read'
#         _dic['param']['read'] = json.dumps(_p)
#
#         track['recommends'].append(_dic)
#
#     track['timestamp'] = temp.time_stamp
#     return track


def feed_recommend(user_id, channel_id, article_num, time_stamp):
    """
    1、根据web提供的参数，进行分流
    2、找到对应的算法组合之后，去推荐中心调用不同的召回和排序服务
    3、进行埋点参数封装
    :param user_id:用户id
    :param article_num:推荐文章个数
    :return: track:埋点参数结果: 参考上面埋点参数组合
    """

    #  产品前期推荐由于较少的点击行为，所以去做 用户冷启动 + 文章冷启动
    # 用户冷启动：'推荐'频道：热门频道的召回+用户实时行为画像召回（在线的不保存画像）  'C2'组合
    #            # 其它频道：热门召回 + 新文章召回   'C1'组合
    # 定义返回参数的类
    class TempParam(object):
        user_id = -10
        channel_id = -10
        article_num = -10
        time_stamp = -10
        algo = ""

    temp = TempParam()
    temp.user_id = user_id
    temp.channel_id = channel_id
    temp.article_num = article_num
    # 请求的时间戳大小
    temp.time_stamp = time_stamp

    # 先读取缓存数据redis+待推荐hbase结果
    # 如果有返回并加上埋点参数
    # 并且写入hbase 当前推荐时间戳用户（登录和匿名）的历史推荐文章列表

    # 传入用户id为空的直接召回结果
    if temp.user_id == "":
        temp.algo = ""
        return add_track([], temp)
    # 进行分桶实现分流，制定不同的实验策略
    bucket = hashlib.md5(user_id.encode()).hexdigest()[:1]
    if bucket in RAParam.BYPASS[0]['Bucket']:
        temp.algo = RAParam.BYPASS[0]['Strategy']
    else:
        temp.algo = RAParam.BYPASS[1]['Strategy']

    # 推荐服务中心推荐结果(这里用add_track封装的方法做测试)
    # track = add_track([], temp)
    track = RecoCenter().feed_recommend_logic(temp)
    return track



# 基于用户推荐的rpc服务推荐
# 定义指定的rpc服务输入输出参数格式proto
class UserRecommendServicer(user_reco_pb2_grpc.UserRecommendServicer):
    """
    对用户进行文章推荐的RPC服务
    """
    def user_recommend(self, request, context):
        """
        用户feed流推荐
        :param request:
        :param context:
        :return:
        """
        # 获取后台传过来的请求参数
        user_id = request.user_id
        channel_id = request.channel_id
        article_num = request.article_num
        time_stamp = request.time_stamp

        # 解析参数，并进行推荐中心推荐(暂时使用假数据替代)

        # 数据测试
        # class Temp(object):
        #     user_id = '1115629498121846784'
        #     algo = 'test'
        #     # 与hbase中的时间单位一致（ms）
        #     time_stamp = int(time.time() * 1000)
        #
        # _track = add_track([1, 2, 3, 4], Temp())

        _track = feed_recommend(user_id, channel_id, article_num, time_stamp)

        # 解析返回参数到rpc结果参数
        # 参数格式如下
        # [       {"article_id": 1, "param": {"click": "", "collect": "", "share": "", 'detentionTime':''}},
        #         {"article_id": 2, "param": {"click": "", "collect": "", "share": "", 'detentionTime':''}},
        #         {"article_id": 3, "param": {"click": "", "collect": "", "share": "", 'detentionTime':''}},
        #         {"article_id": 4, "param": {"click": "", "collect": "", "share": "", 'detentionTime':''}}
        #     ]
        # 构造第二个rpc参数
        _param1 = []
        for _ in _track['recommends']:
            # param的封装
            _params = user_reco_pb2.param2(click=_['param']['click'],
                                           collect=_['param']['collect'],
                                           share=_['param']['share'],
                                           read=_['param']['read'])
            _p2 = user_reco_pb2.param1(article_id=_['article_id'], params=_params)
            _param1.append(_p2)
        # param
        return user_reco_pb2.Track(exposure=_track['param'], recommends=_param1, time_stamp=_track['timestamp'])

#    def article_recommend(self, request, context):
#        """
#       文章相似推荐
#       :param request:
#       :param context:
#       :return:
#       """
#       # 获取web参数
#       article_id = request.article_id
#       article_num = request.article_num
#
#        # 进行文章相似推荐,调用推荐中心的文章相似
#       _article_list = article_reco_list(article_id, article_num, 105)
#
#       # rpc参数封装
#       return user_reco_pb2.Similar(article_id=_article_list)


def serve():
    # 打印日志
    lg.create_logger()

    # 多线程服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 注册本地服务
    user_reco_pb2_grpc.add_UserRecommendServicer_to_server(UserRecommendServicer(), server)
    # 监听端口
    server.add_insecure_port(DefaultConfig.RPC_SERVER)

    # 开始接收请求进行服务
    server.start()
    # 使用 ctrl+c 可以退出服务
    _ONE_DAY_IN_SECONDS = 60 * 60 * 24
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    # 测试grpc服务
    serve()
