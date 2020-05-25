#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/21 20:50
# @Author  : Durat
# @Email   : durant.zeng@sunvalley.com.cn
# @File    : test.py
# @Software: PyCharm
import sys, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import hashlib
import time
import datetime
import random
import string
import sys, os
import re
from jsonpath import jsonpath


class baseUtils:

    def __init__(self):
        pass
        # self.logger = Logger(logger="baseUtils").getlog()

    def MD5(self, str):
        '''
        :param str:
        :return: MD5 encryption
        '''
        m = hashlib.md5()
        b = str.encode(encoding='utf-8')
        m.update(b)
        str_md5 = m.hexdigest()
        return str_md5

    def getTimeStamp(self):
        '''
        :return: str
        '''
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tempList = now.split(" ")
        return ("".join(tempList[0].split("-")) + "".join(tempList[1].split(":")))

    def timestamp_to_str(self, timeStamp=None, format='%Y-%m-%d %H:%M:%S'):
        if timeStamp:
            time_tuple = time.localtime(timeStamp)  # 把时间戳转换成时间元祖
            result = time.strftime(format, time_tuple)  # 把时间元祖转换成格式化好的时间
            return result
        else:
            return time.strptime(format)

    def str_to_timestamp(self, str_time=None, format='%Y-%m-%d %H:%M:%S'):
        if str_time:
            time_tuple = time.strptime(str_time, format)  # 把格式化好的时间转换成元祖
            result = time.mktime(time_tuple)  # 把时间元祖转换成时间戳
            return int(result)
        return int(time.time())

    def get_random_string(self, number):
        '''只能产生最多50'''
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, number))
        return ran_str

    def get_millisecond(self):
        millis = int(round(time.time() * 1000))
        return millis

    def get_miniRectWidth(self):
        number = random.randint(100, 130)
        return number

    def str2int(self, str):
        return int(str)

    def getToDay(self):
        return datetime.date.today()

    def chooseTwoAgentId(self, dict):
        if dict["supplierCompanyName"] == "深圳市丹芽科技":
            return dict["twoAgentId"]
        else:
            return None

    def choosePlan(self, dict):
        if dict["title"] == "美甲机租赁":
            return dict["id"]
        else:
            return None

    def getProjectPath(self):
        # projectName = "AnjouAutotest"
        projectName = "AutoUpLoad"
        projectPath = os.path.dirname(os.path.abspath('.'))
        print("os.path.abspath('.'):", os.path.abspath('.'))
        print("projectPath:", projectPath)
        aList = projectPath.split(projectName)
        bList = aList[0].split(os.sep)
        reallyProject = os.sep.join(bList[0:-1]) + os.sep + projectName
        print("reallyProject:", reallyProject)
        return reallyProject

    def get_deviceID(self, dict):
        result = []
        try:
            data = dict.get('data')
            for lst in data:
                res = lst.get('sn')
                if res != None:
                    result.append(lst.get('id'))
        except:
            raise Exception('error')
        finally:
            return result

    def get_nailSuitStatus_for_1(self, dict):
        result = []
        try:
            data = dict.get('data')
            for lst in data:
                res = lst.get('nailSuitStatus')
                if res == 1:
                    result.append(lst.get('albumsId'))
        except:
            raise Exception('error')
        finally:
            return result

    def get_toUpLoad_dir_list(self, path):
        '''获取将要上传的数据列表'''
        toUpload_dir = [lists for lists in os.listdir(path) if os.path.isdir(os.path.join(path, lists))]
        # self.logger.info("要上传的文件列表为%s" %toUpload_dir)
        return toUpload_dir

    def get_toUpLoad_data_list(self, path):
        '''获取将要上传数据'''
        fileName = [lists for lists in os.listdir(path) if os.path.isfile(os.path.join(path, lists))]
        return fileName

    def get_album_Business_ID_list(self, album_list):
        '''从将要上传的目录获取到特辑的业务ID列表'''
        Business_ID_list = []
        for album in album_list:
            Business_ID = album.split("_")[0]
            Business_ID_list.append(Business_ID)
        return Business_ID_list

    def get_Waterfall_cover(self, picList):
        '''获取瀑布流封面图列表'''
        # 这里只选取固定的666
        Waterfall_cover_list = []
        for pic in picList:
            matchOBJ = re.search(r"666", pic)
            if matchOBJ:
                Waterfall_cover_list.append(pic)
        return Waterfall_cover_list[0]

    def get_album_cover(self, piclist):
        '''获取特辑封面图'''
        album_cover_list = []
        for pic in piclist:
            matchOBJ = re.search(r"1125", pic)
            if matchOBJ:
                album_cover_list.append(pic)
        return album_cover_list[0]

    def get_album_Basemap(self, piclist):
        '''获取特辑的底图'''
        album_Basemap_list = []
        for pic in piclist:
            matchOBJ = re.search(r"1125|666|501", pic)
            if not matchOBJ:
                album_Basemap_list.append(pic)
        return album_Basemap_list[0]

    def get_designer(self, dict_type, authorNickname):
        '''获取设计师的信息'''
        designer = []
        designer_list = dict_type["data"]
        for x in designer_list:
            if x.get("authorNickname") == authorNickname:
                designer.append(x)
        return designer

    def get_designer_really(self, list_type):
        designer = list_type[0]

        designerPra = {
            "authorNickname": designer.get("authorNickname"),
            "authorHeadPortrait": designer.get("authorHeadPortrait"),
            "authorHeadPortraitThumbnail": designer.get("authorHeadPortraitThumbnail"),
            "designerId": designer.get("id")
        }
        return designerPra

    def get_waterFlow_parameters(self, dict_type):
        '''获取瀑布流封面图的发送参数并且组装真正的参数'''

        pictureWidth = jsonpath(dict_type, '$..pictureWidth')
        pictureHeight = jsonpath(dict_type, '$..pictureHeight')
        pictureUrl = jsonpath(dict_type, '$..pictureUrl')
        thumbnailPictureUrl = jsonpath(dict_type, '$..thumbnailPictureUrl')
        parameters = {
            "waterfallFlowUrl": pictureUrl[0],
            "waterfallFlowThumbnailUrl": thumbnailPictureUrl[0],
            "waterfallFlowWidth": pictureWidth[0],
            "waterfallFlowHeight": pictureHeight[0]
        }
        return parameters

    def get_albumCover_parameters(self, dict_type):
        '''获取特辑封面图的发送参数并且组装真正的参数'''

        pictureWidth = jsonpath(dict_type, '$..pictureWidth')
        pictureHeight = jsonpath(dict_type, '$..pictureHeight')
        pictureUrl = jsonpath(dict_type, '$..pictureUrl')
        thumbnailPictureUrl = jsonpath(dict_type, '$..thumbnailPictureUrl')
        pictureName = jsonpath(dict_type, '$..pictureName')
        parameters = {
            "galleryUrl": pictureUrl[0],
            "galleryThumbnailUrl": thumbnailPictureUrl[0],
            "galleryWidth": pictureWidth[0],
            "galleryHeight": pictureHeight[0],
            "galleryName": pictureName[0]
        }
        return parameters

    def get_album_basemap_parameters(self, dict_type):
        '''
        获取特辑底图的参数
        :param dict_type:
        :return:
        '''
        thumbnailPictureUrl = jsonpath(dict_type, '$..thumbnailPictureUrl')
        return thumbnailPictureUrl[0]

    def get_albumPic_parameters(self, dict_type, Order):
        '''获取特辑图片的发送参数并且组装真正的参数'''

        pictureName = jsonpath(dict_type, '$..pictureName')
        pictureUrl = jsonpath(dict_type, '$..pictureUrl')
        thumbnailPictureUrl = jsonpath(dict_type, '$..thumbnailPictureUrl')
        pictureWidth = jsonpath(dict_type, '$..pictureWidth')
        pictureHeight = jsonpath(dict_type, '$..pictureHeight')
        parameters = {
            "galleryName": pictureName[0],
            "galleryUrl": pictureUrl[0],
            "galleryThumbnailUrl": thumbnailPictureUrl[0],
            "galleryOrder": Order,
            "galleryWidth": pictureWidth[0],
            "galleryHeight": pictureHeight[0]
        }
        return parameters

    def get_imagesFalls_parameters(self, dict_type):
        '''
        获取笔记封面图和缩略图
        :param dict_type:
        :return:list
        '''
        pictureUrl = jsonpath(dict_type, '$..pictureUrl')
        thumbnailPictureUrl = jsonpath(dict_type, '$..thumbnailPictureUrl')

        parameters_list = [pictureUrl[0], thumbnailPictureUrl[0]]
        return parameters_list

    def get_imagesUrls_parameters(self, dict_type):
        '''
        获取笔记图和缩略图
        :param dict_type:
        :return:tuple
        '''
        pictureUrl = jsonpath(dict_type, '$..pictureUrl')
        # thumbnailPictureUrl = jsonpath(dict_type, '$..thumbnailPictureUrl')
        return pictureUrl[0]

        # pictureUrl_list = []
        # pictureUrl_list.append(pictureUrl[0])
        # thumbnailPictureUrl_list = []
        # thumbnailPictureUrl_list.append(thumbnailPictureUrl[0])

        # return pictureUrl_list

    def get_imagesLitimgUrls_parameters(self, dict_type):
        '''
        获取笔记图和缩略图
        :param dict_type:
        :return:tuple
        '''
        # pictureUrl = jsonpath(dict_type,'$..pictureUrl')
        thumbnailPictureUrl = jsonpath(dict_type, '$..thumbnailPictureUrl')

        return thumbnailPictureUrl[0]
        # pictureUrl_list = []
        # pictureUrl_list.append(pictureUrl[0])
        # thumbnailPictureUrl_list = []
        # thumbnailPictureUrl_list.append(thumbnailPictureUrl[0])
        #
        # return thumbnailPictureUrl_list

    def get_gallyPic_parameters(self, dict_type, tagIds):
        '''获取系统图库的发送参数并且组装真正的参数'''

        pictureName = jsonpath(dict_type, '$..pictureName')
        pictureUrl = jsonpath(dict_type, '$..pictureUrl')
        thumbnailPictureUrl = jsonpath(dict_type, '$..thumbnailPictureUrl')

        parameters = {
            "galleryName": pictureName[0],
            "galleryUrl": pictureUrl[0],
            "galleryThumbnailUrl": thumbnailPictureUrl[0],
            "isReleaseRemind": 0,
            "tagIds": tagIds,
            "weight": 0
        }
        return parameters

    def get_creator_parameters(self, dict_type):
        '''获取笔记创建者的发送参数并且组装真正的参数'''

        id = jsonpath(dict_type, '$..id')
        uid = jsonpath(dict_type, '$..uid')
        nickname = jsonpath(dict_type, '$..nickname')
        headPortrait = jsonpath(dict_type, '$..headPortrait')
        headPortraitThumbnail = jsonpath(dict_type, '$..headPortraitThumbnail')

        parameters = {
            "creatorId": id[0],
            "creatorUid": uid[0],
            "creatorName": nickname[0],
            "creatorRealName": "",
            "creatorPortrait": headPortrait[0],
            "creatorPortraitLitimg": headPortraitThumbnail[0]
        }
        return parameters

    def get_notes_images_parameters(self, dict_type):
        '''获取笔记图片的发送参数并且组装真正的参数'''

        id = jsonpath(dict_type, '$..id')
        uid = jsonpath(dict_type, '$..uid')
        nickname = jsonpath(dict_type, '$..nickname')
        headPortrait = jsonpath(dict_type, '$..headPortrait')
        headPortraitThumbnail = jsonpath(dict_type, '$..headPortraitThumbnail')

        parameters = {
            "creatorId": id[0],
            "creatorUid": uid[0],
            "creatorName": nickname[0],
            "creatorRealName": "",
            "creatorPortrait": headPortrait[0],
            "creatorPortraitLitimg": headPortraitThumbnail[0]
        }
        return parameters

    def get_Tag_ID(self, dict_type):
        '''获取特辑的ID'''
        Tag_ID = jsonpath(dict_type, '$..id')
        return Tag_ID

    def get_Topic_or_album_ID(self, dict_type):
        '''获取话题或专辑的ID'''
        Topic_ID = jsonpath(dict_type, '$..id')
        return Topic_ID[0]

    def get_albumsContent_really(self, name, description, url1):
        '''
        组装专辑内容的真正参数
        :param name:
        :param description:
        :param url1:
        :param env:
        :return:
        '''

        test = "<p><span style=\"font-family: verdana, geneva, sans-serif; color: #303630;\"><strong><span style=\"font-size: 18px;\">%s</span></strong></span></p>\n<p><span style=\"font-family: verdana, geneva, sans-serif; color: #303630;\">%s</span></p>\n<p><img class=\"wscnph\" src=\"%s\" /></p>" % (
        name, description, url1)
        return test

    def get_album_authorDescribe(self, dict_type, authorNickname):
        '''
        获取专辑作者描述
        :param dict_type:
        :return:
        '''
        authorDescribe = []
        designer_list = dict_type["data"]
        for x in designer_list:
            if x.get("authorNickname") == authorNickname:
                authorDescribe.append(x.get("authorDescribe"))
        return authorDescribe[0]

    # def get_albumsDescribe_really(self,name,description,url1,url2):
    #     '''
    #     组装专辑描述的真正参数
    #     :param name:
    #     :param description:
    #     :param url1:
    #     :param url2:
    #     :return:
    #     '''
    #
    #     test = "<p><span style=\"font-family: verdana, geneva, sans-serif; color: #303630;\"><strong><span style=\"font-size: 18px;\">%s</span></strong></span></p>\n<p><span style=\"font-family: verdana, geneva, sans-serif; color: #303630;\">%s</span></p>\n<p><img class=\"wscnph\" src=\"%s\" /></p><p><img class=\"wscnph\" src=\"%s\" /></p>" %(name,description,url1,url2)
    #     return test

    def get_album_content_url_really(self, env, url):

        baseurl = ""
        if env == "dev":
            baseurl = "https://cdn-dev.nailtutu.com"
        elif env == "uat":
            baseurl = "https://cdn-uat.nailtutu.com"
        elif env == "prod":
            baseurl = "https://cdn.nailtutu.com"
        else:
            print("传入参数有误,请重新检查")

        return baseurl + url


if __name__ == "__main__":
    BU = baseUtils()
    BU.getProjectPath()
    upLoadDir = "D:\AutoUpLoad\data\特辑套图"
    path = BU.get_toUpLoad_dir_list(upLoadDir)
    print(path)
    rt = BU.get_album_Business_ID_list(path)
    print(rt)
    data = BU.get_toUpLoad_data_list("D:\AutoUpLoad\data\特辑套图\T336F_艳阳花开")
    print(data)
    # print(BU.getTimeStamp())
    # path = "D:\learn\AutoUpLoad\data\特辑套图"
    # test = BU.get_toUpLoad_album_list(path)
    # print(test)
    # print(type(test))
    # re = BU.get_Waterfall_size_list(path,test[0])
    # print(re)
    # BU.get_Waterfall_Pic_list()
    # re = BU.get_album_Business_ID_list(test)

    # for i in re:
    #     print(i)
    # test1 = BU.get_toUpLoad_album_data(path)
    # print(test1)
    # test3 = BU.getProjectPath()
    # print(test3)

    # test_list = ['T336F_yanyanghuakai1125.jpg', 'T336F_yanyanghuakai501.jpg', 'T336F_yanyanghuakai666.jpg', 'T336F_yanyanghuakai_y.jpg']
    # mm = BU.get_album_Basemap(test_list)
    # print(mm)
    # mm1 = BU.get_album_cover(test_list)
    # print(mm1)

    # name = "蓝色女人"
    # description = "蓝色女人蓝色女人蓝色女人蓝色女人蓝色女人蓝色女人蓝色女人蓝色女人蓝色女人"
    # URL = "https://cdn-uat.nailtutu.com/tutu/system/20200415114134235_625039.jpg_500x500.jpg"
    # url1 = "https://cdn-uat.nailtutu.com/tutu/system/20200326110832757_320402.jpg_500x500.jpg"
    # res = BU.get_albumsDescribe_really(name,description,URL,url1)
    # print(res)
#     test = {
# 	'stateCode': 200,
# 	'stateMsg': 'OK',
# 	'currentPage': 1,
# 	'pageSize': 4,
# 	'totalNum': 4,
# 	'totalPage': 1,
# 	'data': [{
# 		'id': '2052232570a34c7bb05198eb820f22c5',
# 		'authorHeadPortrait': '/tutu/system/20200326111013054_081463.jpg',
# 		'authorHeadPortraitThumbnail': '/tutu/system/20200326111013054_081463.jpg_512x512.jpg',
# 		'authorNickname': 'carsey',
# 		'authorDescribe': '<p><img class="wscnph" src="https://cdn-uat.nailtutu.com/tutu/system/20200326111029279_575374.jpg_500x500.jpg" /></p>',
# 		'status': 1,
# 		'creatorId': '0463372db7ce402ab6f99574cc4d8d09',
# 		'creatorName': 'admin@sunvalley.com.cn',
# 		'createTime': '2020-03-26 11:10:45',
# 		'modifierId': '',
# 		'modifierName': '',
# 		'modifyTime': '2020-03-26 11:10:45'
# 	}, {
# 		'id': '21d8e8d27d2d4f8999369307999a671c',
# 		'authorHeadPortrait': '/tutu/system/20200326105707181_787550.jpg',
# 		'authorHeadPortraitThumbnail': '/tutu/system/20200326105707181_787550.jpg_512x512.jpg',
# 		'authorNickname': 'mona',
# 		'authorDescribe': '<p><img class="wscnph" src="https://cdn-uat.nailtutu.com/tutu/system/20200326110910581_072840.jpg_500x500.jpg" /></p>',
# 		'status': 1,
# 		'creatorId': '0463372db7ce402ab6f99574cc4d8d09',
# 		'creatorName': 'admin@sunvalley.com.cn',
# 		'createTime': '2020-03-26 10:57:55',
# 		'modifierId': '0463372db7ce402ab6f99574cc4d8d09',
# 		'modifierName': 'admin@sunvalley.com.cn',
# 		'modifyTime': '2020-03-26 11:09:26'
# 	}, {
# 		'id': '9ba2997c095041e38f69637a030603ec',
# 		'authorHeadPortrait': '/tutu/system/20200326110811575_555238.jpg',
# 		'authorHeadPortraitThumbnail': '/tutu/system/20200326110811575_555238.jpg_512x512.jpg',
# 		'authorNickname': 'meira',
# 		'authorDescribe': '<p><img class="wscnph" src="https://cdn-uat.nailtutu.com/tutu/system/20200326110832757_320402.jpg_500x500.jpg" /></p>',
# 		'status': 1,
# 		'creatorId': '0463372db7ce402ab6f99574cc4d8d09',
# 		'creatorName': 'admin@sunvalley.com.cn',
# 		'createTime': '2020-03-26 11:08:41',
# 		'modifierId': '',
# 		'modifierName': '',
# 		'modifyTime': '2020-03-26 11:08:41'
# 	}, {
# 		'id': '9f74564415f0421c81a30132cccb4b7c',
# 		'authorHeadPortrait': '/tutu/system/20200326110612342_078704.jpg',
# 		'authorHeadPortraitThumbnail': '/tutu/system/20200326110612342_078704.jpg_512x512.jpg',
# 		'authorNickname': 'Olia',
# 		'authorDescribe': '<p><img class="wscnph" src="https://cdn-uat.nailtutu.com/tutu/system/20200326110731818_824806.jpg_500x500.jpg" /></p>',
# 		'status': 1,
# 		'creatorId': '0463372db7ce402ab6f99574cc4d8d09',
# 		'creatorName': 'admin@sunvalley.com.cn',
# 		'createTime': '2020-03-26 11:07:43',
# 		'modifierId': '',
# 		'modifierName': '',
# 		'modifyTime': '2020-03-26 11:07:43'
# 	}]
# }
#
#     res = BU.get_album_authorDescribe(test,"Olia")
#     print(res)
