import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import json
import requests
from common.baseUtil import baseUtils
from common.Logger import Logger


class addAlbumsInfo:

    def __init__(self):
        self.logger = Logger(logger="addAlbumsInfo").getlog()
        self.base = baseUtils()

    def get_addAlbumsInfoURL(self,env,access_token):
        '''
        :param baseURL:
        :param lang:
        :param timeStamp:
        :param clientVersionInfo:
        :return:
        '''
        URL = "/oc/tOcAlbumsInfo/addAlbumsInfo"
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


    def send_request_addAlbumsInfo(self,url,designer,albumsTitle,bussinessId,albumsDescribe,albumsContent,waterfallFlow,albumcover,pictureList):
        '''
        添加特辑
        :param url:
        :param status:
        :param currentPage:
        :param pageSize:
        :param authorNickname:
        :return:
        '''
        headers = {"Content-Type": "application/json"}
        parameters = {
                "albumsTitle":albumsTitle,
                "bussinessId":bussinessId,
                "albumsDescribe":albumsDescribe,
                "albumsContent":albumsContent,
                "pictureList":pictureList
                }
        parameters.update(waterfallFlow)
        parameters.update(albumcover)
        parameters.update(designer)

        self.logger.info("请求的参数为:%s" %parameters)
        r = requests.post(url, data=json.dumps(parameters), headers=headers,timeout=30)
        self.logger.info("返回的参数为:%s" % json.loads(r.text))
        return json.loads(r.text)
