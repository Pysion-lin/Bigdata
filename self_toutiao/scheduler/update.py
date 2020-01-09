
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from scheduler import main

def test_compute():
    main.updata_article_profile()

# 创建执行器
executor = {'default':ProcessPoolExecutor(3)}
# 创建调度器
scheduler = BlockingScheduler(executors=executor)
# 设置触发器和任务存储
scheduler.add_job(test_compute,trigger='interval',hours=2)
# 启动定时任务
scheduler.start()