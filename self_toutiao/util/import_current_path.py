import os
import sys
def add_current_path(path):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(path)))
    sys.path.insert(0,BASE_DIR)


