import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from configparser import ConfigParser
from common.Logger import Logger



class FileParser:

    def __init__(self, fileName):
        '''
        :param fileName:
        '''
        self.logger = Logger(logger="FileParser").getlog()
        try:
            self.config = ConfigParser()
            self.config.read(fileName, encoding='gbk')
        except:
            self.logger.info(fileName)
            self.logger.exception('文件名不存在,请检查配置!')


    def get(self, section, option):
        '''
        :param section:
        :param option:
        :return:value
        '''
        res = self.config.get(section, option)
        if  res.strip()== '':
            return False
        else:
            return res


    def set(self,section,option):
        return self.config.set(section, option)


    def get_sections(self):
        '''返回所有的sections'''
        return self.config.sections()



if __name__ == "__main__":
    config = FileParser(r'D:\learn\AutoUpLoad\data\笔记套图\notes.ini')
    dev = config.get("T341F","topic")
    print(type(dev))
    print(dev)


