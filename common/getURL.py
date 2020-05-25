import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from common.Logger import Logger
from common.baseUtil import baseUtils
base = baseUtils()

class GetURL:

    def __init__(self):
        self.logger = Logger(logger="GetURL").getlog()

    def get_url(self,type):
        '''
        :param type:
        :return:
        '''
        if type == "Album":
            url = "/oc/tOcAlbumsInfo/addAlbumsInfo"
            self.logger.info("Album的url为：%s" %url)
        elif type == "uat":
            url = "https://oc-api-uat.nailtutu.com/oauth/login"
            self.logger.info("oc_web登录的url为：%s" % url)
        elif type == "dev":
            url = "https://oc-api-dev.nailtutu.com/oauth/login"
            self.logger.info("oc_web登录的url为：%s" % url)
        else:
            self.logger.error("传值有误，请检查！")
        return url