import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR))
sys.path.insert(0, os.path.join(BASE_DIR, 'reco_sys'))
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from scheduler.update import update_article_profile
from scheduler.update import update_user_profile
from scheduler.update import update_recall
from scheduler.update import update_ctr_feature
# import setting.logging as lg
from settings import logging as lg
lg.create_logger()


# 编写定时运行配置
# 创建scheduler，多进程执行
executors = {
    'default': ProcessPoolExecutor(3)
}

scheduler = BlockingScheduler(executors=executors)

# 添加定时更新任务更新文章画像,每隔一小时更新
scheduler.add_job(update_article_profile, trigger='interval', hours=1)
# 添加定时更新任务更新用户画像，每隔2小时更新
scheduler.add_job(update_user_profile, trigger='interval', hours=2)
# 添加定时更新任务更新离线召回数据，每隔3小时更新
scheduler.add_job(update_recall, trigger='interval', hours=3)
# 添加定时更新任务更新用户和文章特征数据，每隔4小时更新
scheduler.add_job(update_ctr_feature, trigger='interval', hours=4)
scheduler.start()
