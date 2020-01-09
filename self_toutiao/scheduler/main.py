import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)

from offline.article_profile_update import UpdateArticle
from offline.logger import Logger
# 导入scheduler设置
def updata_article_profile():
    Logger('update_article').get_log().debug('ready')
    ua = UpdateArticle()
    Logger('update_article').get_log().debug('create_compolit')
    sentence_df = ua.merge_article_data()
    Logger('update_article').get_log().debug('sentence_df is ok')
    if sentence_df.rdd.collect():
        text_rank_res = ua.generate_article_label(sentence_df)
        article_profile = ua.get_article_profile(text_rank_res)
# 定义文章画像更新的主函数
