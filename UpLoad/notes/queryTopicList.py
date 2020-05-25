import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import json
import requests
from common.baseUtil import baseUtils
from common.Logger import Logger



class queryTopicList:

    def __init__(self):
        self.logger = Logger(logger="queryTopicList").getlog()
        self.base = baseUtils()

    def get_queryTopicListURL(self,env,access_token):
        '''
        :param baseURL:
        :param lang:
        :param timeStamp:
        :param clientVersionInfo:
        :return:
        '''
        URL = "/oc/ugc/topic/queryTopicList"

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



    def send_request_queryTopicList(self,url,title):
        '''
        话题查询列表
        :param url:
        :param title:
        :return:
        '''
        headers = {"Content-Type": "application/json"}

        parameters = {
                    "introduce": "",
                    "title": title,
                    "topicStatus": 1,
                    "currentPage": 1,
                    "pageSize": "20"
            }
        self.logger.info("请求的参数为:%s" %parameters)
        r = requests.post(url, data=json.dumps(parameters), headers=headers,timeout=30)
        self.logger.info("返回的参数为:%s" % json.loads(r.text))
        return json.loads(r.text)