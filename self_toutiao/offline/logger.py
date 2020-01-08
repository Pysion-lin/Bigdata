import logging
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = os.path.join(BASE_DIR,'logs')

class Logger(object):
    def __init__(self,loggername):
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(logging.DEBUG)
        logname = log_path + 'out.log'
        
