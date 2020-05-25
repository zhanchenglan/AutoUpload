import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import json
import requests
from common.baseUtil import baseUtils
from common.Logger import Logger


class queryDesignerList:

    def __init__(self):
        self.logger = Logger(logger="queryDesignerList").getlog()
        self.base = baseUtils()

    def get_queryDesignerListURL(self,env,access_token):
        '''
        :param baseURL:
        :param lang:
        :param timeStamp:
        :param clientVersionInfo:
        :return:
        '''
        URL = "/oc/designer/queryDesignerList"
        if env == "dev":
            baseurl = "https://oc-api-dev.nailtutu.com"
        elif env == "uat":
            baseurl = "https://oc-api-uat.nailtutu.com"
        elif env == "prod":
            baseurl = "https://oc-api.nailtutu.com"
        else:
            self.logger.info("你输入的参数有误，请检查配置")

        ReallyURL = baseurl + URL + "?access_token=%s&lang=zh&timeStamp=%s" % (access_token,self.base.getTimeStamp())
        self.logger.info("url为:%s" %ReallyURL)
        return ReallyURL



    def send_request_queryDesignerList(self,url,authorNickname=None):
        '''
        获取设计师列表
        :param url:
        :param status:
        :param currentPage:
        :param pageSize:
        :param authorNickname:
        :return:
        '''
        headers = {"Content-Type": "application/json"}
        parameters = {
                "status":1,
                "currentPage":1,
                "pageSize":15,
                "authorNickname":authorNickname
                }
        self.logger.info("请求的参数为:%s" %parameters)
        r = requests.post(url, data=json.dumps(parameters), headers=headers,timeout=30)
        self.logger.info("返回的参数为:%s" % json.loads(r.text))
        return json.loads(r.text)