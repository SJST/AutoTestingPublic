'''
Created on 2020年10月26日

@author: Administrator
'''
import sys
import os
print(sys.path)
import time
from lmk_app import  Contants
from _ast import arg
class StrMethod(object):
    '''
     处理字符串的公共方法
    '''
    Data = None # 接收处理后的数据

    def __init__(self, *arg):
        print(sys.path)
        if arg:
            self.data = arg[Contants.SystemContants.Zero] 
        
        '''
        Constructor
        '''
    def format_time_to_str(self):
        '''
                         将时间戳转化为字符串 不需要传参
          :return 字符串时间 
    '''
        self.data = int(time.time())
        timeArray = time.localtime(self.data)
        self.Data = time.strftime( Contants.SystemContants.FormatTime, timeArray)
        print(self.Data)
        print(type(self.Data))
        return self.Data
if __name__ == '__main__':
    TestA = StrMethod()
    data = TestA.format_time_to_str()
    print(data)