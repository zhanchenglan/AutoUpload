import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import fontTools
from common.Logger import Logger



class AnjouFont:

    def __init__(self):
        '''
        :param fileName:
        '''
        self.logger = Logger(logger="AnjouFont").getlog()


    def get(self):
        '''
        :param section:
        :param option:
        :return:value
        '''
        fontTools
        # return self.config.get(section, option