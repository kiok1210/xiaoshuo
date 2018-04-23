# -*- coding: UTF-8 -*-
from urllib import request
from urllib.parse import quote
from bs4 import BeautifulSoup
import os
import threading
import re
import ssl

'''
将爬虫常用工具提取出来
version:0.1 
author:yaowei
date:2018-04-12
'''


class Soup:

    ssl._create_default_https_context = ssl._create_unverified_context

    _HEAD = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, '
                      'like Gecko) Chrome/18.0.1025.166  Safari/535.19'}
    _HEAD2 = {
      'Accept-language': 'zh-CN,zh;q=0.9'
     , 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    @staticmethod
    def get_soup(query_url):
        req = request.Request(quote(query_url, safe='/:?='), headers=Soup._HEAD2)
        webpage = request.urlopen(req)
        html = webpage.read()
        # soup = BeautifulSoup(html, 'html.parser')
        soup = BeautifulSoup(html, 'html5lib')
        return soup

    @staticmethod
    def create_folder(path):
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        rstr = r"[\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_path = re.sub(rstr, "_", path)  # 替换为下划线
        is_exists = os.path.exists(new_path)
        # 不存在则创建
        if not is_exists:
            os.makedirs(new_path)
            print('目录:', new_path + ' create')
        else:
            print(new_path + ' 目录已存在')

    # end createFolder  ---------------------------------------

    @staticmethod
    def is_file(path):
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        rstr = r"[\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_path = re.sub(rstr, "_", path)  # 替换为下划线
        isfile = os.path.exists(new_path)
        if isfile:
            print(new_path, '已存在')
            return ''
        else:
            return new_path

    @staticmethod
    def purge_file(path):
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        rstr = r"[\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_path = re.sub(rstr, "_", path)  # 替换为下划线
        return new_path

    @staticmethod
    def write_file(file_name, content):
        file_object = open(file_name, 'w', encoding='utf-8')
        file_object.write(content)
        file_object.close()


class MyThread(threading.Thread):

    def __init__(self, func, args, name):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name

    def run(self):
        self.func(*self.args)
