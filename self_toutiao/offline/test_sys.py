# encoding=utf-8
import sys
import os
import platform
BASE_DIR = os.path.dirname(os.getcwd())
sys.path.insert(0,os.path.join(BASE_DIR))


# 导包路径
# print(os.path)
#
#环境变量
print(os.environ)
# Python版本号
# print(platform.python_version())

# 内核路径
print(sys.executable)