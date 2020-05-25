import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import json
import requests
from common.baseUtil import baseUtils
from common.Logger import Logger



class addArticle:

    def __init__(self):
        self.logger = Logger(logger="addArticle").getlog()
        self.base = baseUtils()

    def get_addArticleURL(self,env,access_token):
        '''
        :param baseURL:
        :param lang:
        :param timeStamp:
        :param clientVersionInfo:
        :return:
        '''
        URL = "/oc/ugc/article/addArticle"

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



    def send_request_addArticle(self,url,content,weight,creator,imagesFalls,imagesUrls,imagesLitimgUrls,topicId=None,albumsId=None):
        '''
        笔记发布
        :param url:
        :param title:
        :return:
        '''
        headers = {"Content-Type": "application/json"}
        videoFalls = {
            "videoFallsUrl":"",
            "videoFallsLitimgUrl":"",
            "videoUrl":"",
            "videoFallsHeight":"",
            "videoFallsWidth":""
        }

        #文章状态 1-草稿, 3-发布,5-待发布;
        parameters = {
                    "articleType": 1,
                    "content": content,
                    "topicId": topicId,
                    "albumsId": albumsId,
                    "articleStatus": 5,
                    "weight":weight,
                    "publishTime":"",
                    "imagesUrls":imagesUrls,
                    "imagesLitimgUrls":imagesLitimgUrls,
                    "imagesFallsUrl":imagesFalls[0],
                    "imagesFallsLitimgUrl":imagesFalls[1]
            }

        #封面信息
        # parameters.update(imagesFalls)
        #视频信息
        # parameters.update(videoFalls)
        #创建者信息
        parameters.update(creator)

        self.logger.info("请求的参数为:%s" %parameters)
        r = requests.post(url, data=json.dumps(parameters), headers=headers,timeout=30)
        self.logger.info("返回的参数为:%s" % json.loads(r.text))
        return json.loads(r.text)