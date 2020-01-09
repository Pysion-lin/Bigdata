import logging
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = os.path.join(BASE_DIR,'logs')
print(log_path)
class Logger(object):
    def __init__(self,loggername):
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(logging.DEBUG)
        logname = log_path + '/out.log'

        fh = logging.FileHandler(logname,encoding='utf-8')
        fh.setLevel(logging.DEBUG)

        ch =logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_log(self):
        return self.logger

if __name__ == "__main__":
    # t = Logger('TEST').get_log().debug('user root debug test')
    Logger('TEST').get_log().info('ad')