#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/27 10:42
# @Author  : Durat
# @Email   : durant.zeng@sunvalley.com.cn
# @File    : run_case.py
# @Software: PyCharm
import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import unittest
from BeautifulReport import BeautifulReport
from interface.base.fileUpload.common import common
from interface.base.login.authentication import Authentication
from common.baseUtil import baseUtils
from common.mysqlUtils import mysqlUtils
from common.FileParsing import FileParser



base = baseUtils()

projectPath = base.getProjectPath() + os.sep + "config" + os.sep + "config.ini"
# print(projectPath)
config = FileParser(projectPath)

# print(config)
# print("初始化配置成功")

host = config.get("mysql_prod","host")
port = config.get("mysql_prod","port")
user = config.get("mysql_prod","user")
password = config.get("mysql_prod","password")
db_platform = config.get("mysql_prod","db_platform")

mysql = mysqlUtils(host,port,user,password,db_platform)

filename = "tutuApplets.html"


# 用例路径
case_path = os.path.join(os.getcwd())
# print(case_path)
# 报告存放路径
report_path = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), 'report')

log_path = base.getProjectPath()+os.sep+"report"+os.sep

def getenv():
    env = sys.argv[1]
    return env



def find_new_file(report_path):
    '''查找目录下最新的文件'''
    file_lists = os.listdir(report_path)
    file_lists.sort(key=lambda fn: os.path.getmtime(report_path + "\\" + fn)
                    if not os.path.isdir(report_path + "\\" + fn) else 0)
    # print('最新的文件为： ' + file_lists[-1])
    file = os.path.join(report_path, file_lists[-1])
    # print('完整路径：', file)
    return file


def all_case():
    #discover = unittest.defaultTestLoader.discover(case_path, pattern="test*.py", top_level_dir=None)
    #discover = unittest.defaultTestLoader.discover(case_path, pattern="testlq.py", top_level_dir=None)
    discover = unittest.defaultTestLoader.discover(case_path, pattern="test_case_*.py", top_level_dir=None)
    # print (discover)
    return discover


def  run(testSuit):
    result = BeautifulReport(testSuit)
    result.report(filename=filename, description='tutuAppletsAutoTest接口自动化测试报告', log_path="../report")
    return result

if __name__ == "__main__":
    testSuit = all_case()
    result = run(testSuit)
    errorNumber = result.error_count
    start_time = result.begin_time
    s = result.start_time
    totalTime = result.stopTestRun().get("totalTime")

    timeStamp = str(s).split(".")[0]
    end_time = base.timestamp_to_str(int(timeStamp))

  #   #  `area` int(1) DEFAULT '1' COMMENT '区域：1-国内，2-国外；',
  # `system_type` int(1) DEFAULT '1' COMMENT '系统类型：1-安卓/pad，2-IOS，3-小程序',
  # `business_type` int(6) DEFAULT NULL COMMENT '业务类型：1-tutu/anjou，2-pad，3-商户端',

    area = 1
    system_type = 3
    business_type = 1
    task_name = "prod-tutuApplets"
    #2 - 执行成功，3 - 执行失败(int类型)

    duration = int(totalTime[0:-1])


    #小程序登录
    AC = Authentication()
    phone = "13417335080"
    password = "123456"
    data = AC.get_Applets_ordinary_logged_in(phone, password)
    Applets_login_url = AC.get_AuthenticationURL(config.get('imi_base_url_ch', 'base_url_prod'),
                                                     config.get("imi_login_url", "login_url"),
                                                     config.get("lang", "zh"), base.getTimeStamp(),
                                                     config.get("clientVersionInfo","clientVersionInfo_ch_Android"))

    access_token = AC.get_Access_token(Applets_login_url, data)


    #调用上传-通用文件接口,返回一个文件的URL,以便存储到mysql，供给OC端解析
    common = common()

    commonURL = common.get_commonURL(config.get('imi_base_url_ch', 'base_url_prod'),
                                                  config.get("fileUpload", "commonURL"), config.get("lang", "zh"),
                                                  base.getTimeStamp(),
                                                  config.get("clientVersionInfo", "clientVersionInfo_ch_Android"),access_token)

    filepath = base.getProjectPath() + os.sep + "report"  + os.sep + filename
    filename = filename
    dictory = "AutoTest/tutuApplets"
    autoWithContentType = True
    print(filename)
    print(filepath)
    result_common = common.send_request_common(commonURL, filename, filepath, dictory,autoWithContentType)


    if result_common["stateCode"] == 200:
        print("测试报告上传到阿里云成功")
        exe_result_content = result_common["data"]["fileUrl"]
        failureNumber = result.failure_count
        error_failure_number = errorNumber + failureNumber
        if error_failure_number == 0:
            exe_result = 2
            mysql.insertInto_autoTest_record(area, system_type, business_type, task_name, start_time, end_time, exe_result,
                                         end_time, duration,exe_result_content)
        else:
            exe_result = 3
            mysql.insertInto_autoTest_record(area, system_type, business_type, task_name, start_time, end_time, exe_result,
                                         end_time, duration,exe_result_content)

    else:
        print("测试报告上传失败")
