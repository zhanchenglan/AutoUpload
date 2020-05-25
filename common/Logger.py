#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/21 20:50
# @Author  : Durat
# @Email   : durant.zeng@sunvalley.com.cn
# @File    : test.py
# @Software: PyCharm
import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import logging
import os.path
import time
from common.baseUtil import baseUtils

class Logger:

    def __init__(self, logger):
        self.base = baseUtils()
        '''
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志存入到指定的文件中
        '''
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.DEBUG)

            # 创建一个handler，用于写入日志文件
            rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
            # log_path = os.path.dirname(os.getcwd()) + '/Logs/'  # 项目根目录下/Logs 保存日志
            # log_path = os.path.dirname(os.path.abspath('.')) + '/logs/'
            log_path = self.base.getProjectPath()+os.sep+"logs"+os.sep
            # print(log_path)
            # log_path = r"D:\anjouAutoTest\logs"
            # 如果case组织结构式 /testsuit/featuremodel/xxx.py ， 那么得到的相对路径的父路径就是项目根目录
            log_name = log_path + rq + '.log'
            # print(log_name)
            # time.sleep(1)
            # if not os.path.isfile(log_name):
            #     fd = open(log_name, mode="w", encoding="utf-8")
            #     fd.close()
            fh = logging.FileHandler(log_name, encoding='utf-8')  # 指定编码为UTF-8,中文乱码问题就可以解决
            fh.setLevel(logging.INFO)

            # 再创建一个handler，用于输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)

            # 定义handler的输出格式
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # 给logger添加handler
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

    def getlog(self):
        return self.logger

# if __name__ == "__main__":
