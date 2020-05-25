import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import os,sys
import random
from common.ocweb import ocweb
from common.baseUtil import baseUtils
from common.FileParsing import FileParser
from fileUpload.single import single
from UpLoad.Album.addAlbumsInfo import addAlbumsInfo
from UpLoad.Album.queryDesignerList import queryDesignerList
from UpLoad.Gallery.queryTagInfo import queryTagInfo
from UpLoad.Gallery.addSystemPic import addSystemPic
from UpLoad.notes.queryUserInfoList import queryUserInfoList
from UpLoad.notes.queryTopicList import queryTopicList
from UpLoad.notes.getAlbumsList import getAlbumsList
from UpLoad.notes.addArticle import addArticle
from common.Logger import Logger


class Start:

    def __init__(self):
        self.logger = Logger(logger="Start").getlog()
        self._Base_Path_Album_config = os.sep + "data" + os.sep + "特辑套图" + os.sep + "Album.ini"
        self._Base_Path_Notes_config = os.sep + "data" + os.sep + "笔记套图" + os.sep + "notes.ini"
        self.oc = ocweb()
        self.base = baseUtils()
        self.config_album = FileParser(self.base.getProjectPath() + self._Base_Path_Album_config)
        self.config_note = FileParser(self.base.getProjectPath() + self._Base_Path_Notes_config)
        self.single = single()
        self.queryDesigner = queryDesignerList()
        self.addAlbums = addAlbumsInfo()
        self.queryTag = queryTagInfo()
        self.addSystemPic = addSystemPic()
        self.queryUserInfo = queryUserInfoList()
        self.queryTopic = queryTopicList()
        self.getAlbumsList = getAlbumsList()
        self.addArticle = addArticle()

    def album_UpLoad(self,Basepath):
        '''
        登录
        获取特辑标题
        获取业务ID
        获取设计师信息
        获取特辑瀑布流封面
        获取特辑封面
        获取特辑图片
        获取特辑内容+特辑内容图片
        调添加特辑接口
        退出登录
        :return:
        '''
        #登录OC
        re = self.oc.login("uat","admin@sunvalley.com.cn","danya@123")
        access_token = re[1]

        #定义将要上传特辑的目录
        ReallyPath = self.base.getProjectPath() + Basepath
        print("特辑上传的根路径")
        print(ReallyPath)

        #获取要上传的特辑列表
        toUpLoad_album_list = self.base.get_toUpLoad_dir_list(ReallyPath)
        print("要上传的特辑列表:",toUpLoad_album_list)

        #获取特辑业务ID列表
        album_Business_ID_list = self.base.get_album_Business_ID_list(toUpLoad_album_list)
        print("特辑业务ID列表:",album_Business_ID_list)

        # 使用列表生成器，快速的拼接特辑列表的绝对路径，返回list
        album_list_abs_path = [ReallyPath + os.sep + x for x in toUpLoad_album_list]
        print("特辑列表的绝对路径:",album_list_abs_path)


        for i in range(len(album_list_abs_path)):

            album_pic_list = self.base.get_toUpLoad_data_list(album_list_abs_path[i])
            print("特辑图片为")
            print(album_pic_list)


            #使用列表生成器，快速的特辑图片文件列表的绝对路径，返回list
            album_pic_list_abs_path = [album_list_abs_path[i] + os.sep + p for p in album_pic_list]
            print("特辑图片的绝对路径为")
            print(album_pic_list_abs_path)

            #选取设计师
            authorNickname = self.config_album.get(album_Business_ID_list[i], "authorNickname")
            queryDesignerURL = self.queryDesigner.get_queryDesignerListURL("uat",access_token)
            queryDesigner_res = self.queryDesigner.send_request_queryDesignerList(queryDesignerURL)
            print("queryDesigner_res:",queryDesigner_res)

            designer = self.base.get_designer(queryDesigner_res,authorNickname)
            print("designer:%s" %designer)
            designer_really = self.base.get_designer_really(designer)
            print("designer_really",designer_really)

            authorDescribe = self.base.get_album_authorDescribe(queryDesigner_res,authorNickname)
            print("专辑作者的描述信息为：")
            print(authorDescribe)


            #获取特辑标题
            album_title = self.config_album.get(album_Business_ID_list[i],"name")
            print(album_title)

            #获取特辑的业务ID
            album_coding = self.config_album.get(album_Business_ID_list[i], "coding")
            print(album_coding)

            # #获取第一张特辑的绝对路径
            # first_abs_path = ReallyPath + os.sep + toUpLoad_album_list[x]
            # print(first_abs_path)

            #瀑布流的文件夹名称
            water_flow_Folder_name = self.base.get_toUpLoad_dir_list(album_list_abs_path[i])
            print("瀑布流的文件夹名称为")
            print(water_flow_Folder_name)

            # 使用列表生成器，快速的拼接瀑布流的文件夹名称的绝对路径，返回list
            water_flow_Folder_name_list_abs_path = [album_list_abs_path[i] + os.sep + y for y in water_flow_Folder_name]
            print("瀑布流的文件夹名称的绝对路径为")
            print(water_flow_Folder_name_list_abs_path)


            # really_firstName = ReallyPath + os.sep + toUpLoad_album_list[0]+os.sep + firstName[0]
            # print(really_firstName)

            #获取瀑布流的文件列表,返回list
            water_flow_pic_list = self.base.get_toUpLoad_data_list(water_flow_Folder_name_list_abs_path[0])
            print(water_flow_pic_list)

            # 使用列表生成器，快速的拼接瀑布流的文件列表的绝对路径，返回list
            water_flow_pic_list_abs_path = [water_flow_Folder_name_list_abs_path[0] + os.sep + z for z in water_flow_pic_list]
            print(water_flow_pic_list_abs_path)



            ##################特辑瀑布流封面################################
            # 获取特辑瀑布流封面图名称
            waterflow_cover_pic = self.base.get_Waterfall_cover(water_flow_pic_list)
            print(waterflow_cover_pic)

            #获取特辑瀑布流封面图的绝对路径
            waterflow_cover_pic_abs_path = self.base.get_Waterfall_cover(water_flow_pic_list_abs_path)
            print(waterflow_cover_pic_abs_path)


            #获取特辑瀑布流封面图,并上传
            singleURL = self.single.get_singleURL("uat",access_token)
            waterflow_res = self.single.send_request_single(singleURL,waterflow_cover_pic,waterflow_cover_pic_abs_path,"WaterfallCover")

            #瀑布流图片的参数值
            waterflow_res_really = self.base.get_waterFlow_parameters(waterflow_res)
            print(waterflow_res_really)


            ##################特辑封面################################
            # 获取特辑封面名称
            album_cover_pic = self.base.get_album_cover(water_flow_pic_list)
            print(album_cover_pic)

            #获取特辑封面的绝对路径
            album_cover_pic_abs_path = self.base.get_album_cover(water_flow_pic_list_abs_path)
            print(album_cover_pic_abs_path)



            # 获取特辑封面图,并上传
            albumCover_res = self.single.send_request_single(singleURL,album_cover_pic,album_cover_pic_abs_path,"albumCover")
            #特辑封面的参数值
            albumCover_res_really = self.base.get_albumCover_parameters(albumCover_res)
            print("特辑封面的参数为：")
            print(albumCover_res_really)




            ##################特辑图片################################
            print("album_pic_list为：%s" %album_pic_list)
            print("album_pic_list_abs_path为：%s" % album_pic_list_abs_path)
            print("..................................................................................................")
            album_pic_list_really = self.get_albumPic_parameters_really(singleURL,album_pic_list,album_pic_list_abs_path)

            print(".......................")
            print(album_pic_list_really)
            print(".......................")


            #获取特辑内容
            album_Description = self.config_album.get(album_Business_ID_list[i],"Description")
            print(album_Description)



            ##################特辑底图################################
            # 获取特辑底图名称
            album_basemap_pic = self.base.get_album_Basemap(water_flow_pic_list)
            print(album_basemap_pic)

            #获取特辑底图的绝对路径
            album_basemap_pic_abs_path = self.base.get_album_Basemap(water_flow_pic_list_abs_path)
            print(album_basemap_pic_abs_path)


            album_basemap_res = self.single.send_request_single(singleURL,album_basemap_pic,album_basemap_pic_abs_path,"AlbumContentPic")
            #特辑底图的参数值
            album_basemap_parameters = self.base.get_album_basemap_parameters(album_basemap_res)
            print("特辑底图的参数为：")
            print(album_basemap_parameters)
            print("结束")
            album_basemap_res = self.base.get_album_content_url_really("uat",album_basemap_parameters)
            albumsContent = self.base.get_albumsContent_really(album_title,album_Description,album_basemap_res)
            print("albumsContent的参数值为%s" %albumsContent)

            albumsDescribe = albumsContent + authorDescribe
            print("albumsDescribe的参数值为%s" % albumsDescribe)



            # #保存特辑
            addAlbumsURL = self.addAlbums.get_addAlbumsInfoURL("uat",access_token)
            self.addAlbums.send_request_addAlbumsInfo(addAlbumsURL,designer_really,album_title,album_Business_ID_list[i],albumsDescribe,albumsContent,waterflow_res_really,albumCover_res_really,album_pic_list_really)

        #退出登陆
        self.oc.logout("uat",access_token)


    def get_albumPic_parameters_really(self,singleURL,album_pic_list,album_pic_list_abs_path):
        '''获取真正发送的特辑图片列表'''
        album_pic_list_really = []
        for x in range(len(album_pic_list)):
            # album_pic_res = self.single.send_request_single(singleURL,album_pic_list,album_pic_list_abs_path,"albumPic")
            album_pic_res = self.single.send_request_single(singleURL,album_pic_list[x],album_pic_list_abs_path[x],"albumPic")
            album_pic = self.base.get_albumPic_parameters(album_pic_res,x+1)
            print(album_pic)
            album_pic_list_really.append(album_pic)
            continue
        return album_pic_list_really

    def get_notePic_parameters_really(self,singleURL,note_pic_list,note_pic_list_abs_path):
        '''获取真正发送的笔记图片参数'''
        imagesFalls_list = []
        imagesUrls_pic_list = []
        imagesLitimgUrls_pic_list = []
        for x in range(len(note_pic_list)):
            note_pic_res = self.single.send_request_single(singleURL,note_pic_list[x],note_pic_list_abs_path[x],"note")
            if x == 0:
                imagesFalls = self.base.get_imagesFalls_parameters(note_pic_res)
                imagesFalls_list.append(imagesFalls)
            imagesUrls_pic = self.base.get_imagesUrls_parameters(note_pic_res)
            imagesUrls_pic_list.append(imagesUrls_pic)
            imagesLitimgUrls_pic = self.base.get_imagesLitimgUrls_parameters(note_pic_res)
            imagesLitimgUrls_pic_list.append(imagesLitimgUrls_pic)
            continue

        return imagesFalls_list[0],imagesUrls_pic_list,imagesLitimgUrls_pic_list



    def get_gallyPic_parameters_really(self,singleURL,gally_pic_list,gally_pic_list_abs_path,tagIds):
        '''获取真正发送的系统图库列表'''
        gally_pic_list_really = []
        for x in range(len(gally_pic_list)):
            gally_pic_res = self.single.send_request_single(singleURL,gally_pic_list[x],gally_pic_list_abs_path[x],"gallery")
            gally_pic = self.base.get_gallyPic_parameters(gally_pic_res,tagIds)
            # print(gally_pic)
            gally_pic_list_really.append(gally_pic)
            continue
        return gally_pic_list_really


    def notes_UpLoad(self,Basepath):
        '''
        登录
        获取标签列表
        比较标签是否存在，不存在则创建，存在则直接上传
        系统图库上传，关联标签
        :return:
        '''
        #登录OC
        re = self.oc.login("uat","admin@sunvalley.com.cn","danya@123")
        access_token = re[1]

        #定义将要上传笔记的目录
        ReallyPath = self.base.getProjectPath() + Basepath

        # 获取要上传的笔记列表
        toUpLoad_notes_list = self.base.get_toUpLoad_dir_list(ReallyPath)
        # print(toUpLoad_notes_list)

        # 使用列表生成器，快速的拼接笔记列表的绝对路径，返回list
        notes_list_abs_path = [ReallyPath + os.sep + x for x in toUpLoad_notes_list]
        # print(notes_list_abs_path)

        #定义要上传的笔记数量
        for x in range(len(notes_list_abs_path)):
            # #获取笔记要上传的图片列表
            note_pic_list = self.base.get_toUpLoad_data_list(notes_list_abs_path[x])
            # print(note_pic_list)

            # 使用列表生成器，快速的拼接笔记图片的绝对路径，返回list
            note_pic_list_abs_path = [notes_list_abs_path[x] + os.sep + y for y in note_pic_list]
            # print(note_pic_list_abs_path)

            singleURL = self.single.get_singleURL("uat", access_token)

            images_really = self.get_notePic_parameters_really(singleURL, note_pic_list, note_pic_list_abs_path)
            # print("笔记的图片参数为%s" % str(images_really))


            #获取创建用户的ID
            queryUserInfoURL = self.queryUserInfo.get_queryUserInfoListURL("uat",access_token)
            queryUserInfo_res = self.queryUserInfo.send_request_queryUserInfoList(queryUserInfoURL,self.config_note.get(toUpLoad_notes_list[x],"authorNickname"))
            creator = self.base.get_creator_parameters(queryUserInfo_res)
            # print(creator)
            # 查询话题ID

            re_topic = self.config_note.get(toUpLoad_notes_list[x], "topic")
            re_album = self.config_note.get(toUpLoad_notes_list[x], "album")
            # 获取权重

            weight = self.config_note.get(toUpLoad_notes_list[x], "weight")
            # print(weight)

            # 获取笔记内容
            content = self.config_note.get(toUpLoad_notes_list[x], "content")
            # print(content)

            if isinstance(re_topic,str) and isinstance(re_album,str):
                queryTopicURL = self.queryTopic.get_queryTopicListURL("uat", access_token)

                queryTopic_res = self.queryTopic.send_request_queryTopicList(queryTopicURL,self.config_note.get(toUpLoad_notes_list[x],"topic"))
                print(queryTopic_res)
                topicID = self.base.get_Topic_or_album_ID(queryTopic_res)
                print(topicID)
                #特辑查询
                getAlbumsListURL = self.getAlbumsList.get_getAlbumsListURL("uat",access_token)
                getAlbumsList_res = self.getAlbumsList.send_request_getAlbumsList(getAlbumsListURL,self.config_note.get(toUpLoad_notes_list[x],"album"))
                print(getAlbumsList_res)
                albumID = self.base.get_Topic_or_album_ID(getAlbumsList_res)
                print(albumID)

                #调用笔记上传接口
                addArticleURL = self.addArticle.get_addArticleURL("uat",access_token)
                self.addArticle.send_request_addArticle(addArticleURL,content,weight,creator,images_really[0],images_really[1],images_really[2],topicID,albumID)

            elif isinstance(re_topic,str) and isinstance(re_album,bool):
                queryTopicURL = self.queryTopic.get_queryTopicListURL("uat", access_token)

                queryTopic_res = self.queryTopic.send_request_queryTopicList(queryTopicURL,self.config_note.get(toUpLoad_notes_list[x],"topic"))
                print(queryTopic_res)
                topicID = self.base.get_Topic_or_album_ID(queryTopic_res)
                print(topicID)
                #特辑查询
                albumID = ""
                #调用笔记上传接口
                addArticleURL = self.addArticle.get_addArticleURL("uat",access_token)
                self.addArticle.send_request_addArticle(addArticleURL,content,weight,creator,images_really[0],images_really[1],images_really[2],topicID,albumID)

            elif isinstance(re_topic, bool) and isinstance(re_album, str):
                topicID = ""
                #特辑查询
                getAlbumsListURL = self.getAlbumsList.get_getAlbumsListURL("uat",access_token)
                getAlbumsList_res = self.getAlbumsList.send_request_getAlbumsList(getAlbumsListURL,self.config_note.get(toUpLoad_notes_list[x],"album"))
                print(getAlbumsList_res)
                albumID = self.base.get_Topic_or_album_ID(getAlbumsList_res)
                print(albumID)
                #调用笔记上传接口
                addArticleURL = self.addArticle.get_addArticleURL("uat",access_token)
                self.addArticle.send_request_addArticle(addArticleURL,content,weight,creator,images_really[0],images_really[1],images_really[2],topicID,albumID)
            elif isinstance(re_topic, bool) and isinstance(re_album, bool):
                topicID = ""
                albumID = ""
                # 调用笔记上传接口
                addArticleURL = self.addArticle.get_addArticleURL("uat", access_token)
                self.addArticle.send_request_addArticle(addArticleURL, content, weight, creator, images_really[0],images_really[1], images_really[2], topicID, albumID)
            else:
                pass

        # 退出登陆
        self.oc.logout("uat", access_token)


    def gally_UpLoad(self,Basepath):
        '''
        登录
        获取标签列表
        比较标签是否存在，不存在则创建，存在则直接上传
        系统图库上传，关联标签
        :return:
        '''
        #登录OC
        re = self.oc.login("uat","admin@sunvalley.com.cn","danya@123")
        access_token = re[1]

        #定义将要系统图库的目录
        ReallyPath = self.base.getProjectPath() + Basepath

        #获取要上传的图库标签列表
        toUpLoad_gally_tag_list = self.base.get_toUpLoad_dir_list(ReallyPath)
        # print(toUpLoad_gally_tag_list)


        # 使用列表生成器，快速的拼接系统图库标签列表的绝对路径，返回list
        gally_tag_list_abs_path = [ReallyPath + os.sep + x for x in toUpLoad_gally_tag_list]
        # print(gally_tag_list_abs_path)


        # #第一个标签的真实路径
        # firstPath = ReallyPath + os.sep + toUpLoad_gally_tag_list[0]
        # print("第一个%s" %firstPath)
        singleURL = self.single.get_singleURL("uat", access_token)


        for x in range(len(gally_tag_list_abs_path)):
            # print(gally_tag_list_abs_path[x])
            gally_pic_list = self.base.get_toUpLoad_data_list(gally_tag_list_abs_path[x])
            # print(gally_pic_list)

            # 使用列表生成器，快速的拼接各系统图库标签下图片的绝对路径，返回list
            gally_pic_list_abs_path = [gally_tag_list_abs_path[x] + os.sep + y for y in gally_pic_list]
            # print(gally_pic_list_abs_path)
            queryTagURL = self.queryTag.get_queryTagInfoURL("uat",access_token)
            queryTag_result = self.queryTag.send_request_queryTagInfo(queryTagURL,toUpLoad_gally_tag_list[x])
            # print(queryTag_result)
            TagID = self.base.get_Tag_ID(queryTag_result)
            # print(TagID)


            #该标签下的所有图片上传，然后关联该标签
            gally_pic_list_really = self.get_gallyPic_parameters_really(singleURL, gally_pic_list, gally_pic_list_abs_path,TagID)
            # print(".......................")
            # print(gally_pic_list_really)
            # print(".......................")

            #保存系统图库
            addSystemPicURL = self.addSystemPic.get_addSystemPicURL("uat",access_token)
            self.addSystemPic.send_request_addSystemPic(addSystemPicURL,gally_pic_list_really)


        # 退出登陆
        self.oc.logout("uat", access_token)



        # #查询标签列表
        # for x in range(len(toUpLoad_gally_tag_list)):
        #     #toUpLoad_gally_tag_list[x]
        #     queryTagURL = self.queryTag.get_queryTagInfoURL("uat",access_token)
        #     queryTag_result = self.queryTag.send_request_queryTagInfo(queryTagURL,toUpLoad_gally_tag_list[x])
        #     print(queryTag_result)
        #     TagID = self.base.get_Tag_ID(queryTag_result)
        #     print(TagID)



        # singleURL = self.single.get_singleURL("uat", access_token)
        #
        # #该标签下的所有图片上传，然后关联该标签
        # gally_pic_list_really = self.get_gallyPic_parameters_really(singleURL, gally_pic_list, gally_pic_list_abs_path,TagID)
        # print(".......................")
        # print(gally_pic_list_really)
        # print(".......................")
        #
        # #保存系统图库
        # addSystemPicURL = self.addSystemPic.get_addSystemPicURL("uat",access_token)
        # self.addSystemPic.send_request_addSystemPic(addSystemPicURL,gally_pic_list_really)
        #
        # # 退出登陆
        # self.oc.logout("uat", access_token)


if __name__ == '__main__':
    start = Start()
    Basepath_album = os.sep + "data" + os.sep + "特辑套图"
    start.album_UpLoad(Basepath_album)

    #ok
    # Basepath_gally = os.sep + "data" + os.sep + "系统图库"
    # start.gally_UpLoad(Basepath_gally)

    # Basepath_notes = os.sep + "data" + os.sep + "笔记套图"
    # start.notes_UpLoad(Basepath_notes)



