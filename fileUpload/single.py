import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import requests
import json
import datetime
from common.Logger import Logger
import warnings


class single:

    def __init__(self):
        self.logger = Logger(logger="single").getlog()
        warnings.simplefilter("ignore",ResourceWarning)


    def getTimeStamp(self):
        '''
        :return: str
        '''
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tempList = now.split(" ")
        return ("".join(tempList[0].split("-")) + "".join(tempList[1].split(":")))


    def get_singleURL(self, env,access_token):
        '''
        上传-单图(缩略图自适应版)
        :param url:
        :param lang:
        :param timeStamp:
        :param clientVersionInfo:
        :return:
        '''
        baseurl = ""
        url = "/file/picture-upload/single"
        if env == "dev":
            baseurl = "https://oc-api-dev.nailtutu.com"
        elif env == "uat":
            baseurl = "https://oc-api-uat.nailtutu.com"
        elif env == "prod":
            baseurl = "https://oc-api.nailtutu.com"
        else:
            self.logger.info("您输入的参数有误，请重新检查")

        ReallyURL = baseurl+ url + "?timeStamp=%s&access_token=%s" % (self.getTimeStamp(),access_token)
        self.logger.info("上传-单图(缩略图自适应版)的URL为:%s" % ReallyURL)
        return ReallyURL

    def send_request_single(self,url,filename,filepath,type):
        '''
        :param url:
        :param filename:
        :param filepath:
        :return:
        '''

        custom_headers = {

        }
        files = {"file":(filename,open(filepath,"rb"),"multipart/form-data",custom_headers)}
        if type == "WaterfallCover":
            upload_data = {"targetid":"4305685b17aa11e9b53f005056ad4128",
                    "sizes":"240x360",
                    "with":360,
                    "height":360,
                    "dpi":120,
                    "quality":0.95,
                    "proportion":3}
        elif type == "albumCover" or type == "AlbumContentPic":
            upload_data = {"targetid":"4305685b17aa11e9b53f005056ad4128",
                    "sizes":"240x360",
                    "with":500,
                    "height":500,
                    "dpi":120,
                    "quality":0.95,
                    "proportion":3}
        elif type == "note":
            upload_data = {"targetid":"4305685b17aa11e9b53f005056ad4128",
                    "sizes":"240x360",
                    "with":100,
                    "height":100,
                    "dpi":120,
                    "quality":0.95,
                    "proportion":3}
        elif type == "albumPic" or type == "gallery":
            upload_data = {"targetid":"4305685b17aa11e9b53f005056ad4128",
                    "sizes":"240x360",
                    "proportion":True}
        else:
            self.logger.info("选择上传的图片类型有误,请重选选择上传")

        self.logger.info("请求参数为%s" %upload_data)
        r = requests.post(url,data = upload_data,files=files,timeout=30)
        # r = requests.request("post", url, data=upload_data, files=files, timeout=30)
        re = r.text
        josnre = json.loads(re)
        self.logger.info("返回值为：%s" %josnre)
        return json.loads(re)
