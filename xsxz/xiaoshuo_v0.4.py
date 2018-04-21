# -*- coding: UTF-8 -*-
from urllib import request
from bs4 import BeautifulSoup
import os
import re

'''
使用BeautifulSoup抓取网页
version:0.4
author:yaowei
date:2018-03-23
'''

class Capture():

    def __init__(self):
        self.index_page_url = 'http://www.cuiweijuxs.com/'
        self.one_page_url = 'http://www.cuiweijuxs.com/jingpinxiaoshuo/'
        self.two_page_url = "http://www.cuiweijuxs.com/jingpinxiaoshuo/5_?.html"
        self.folder_path = '绯色/'
        self.head = {}
        self.threads = []
        # 写入User Agent信息
        self.head[
            'User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
    # end __init__ ---------------------------------------

    # 获取BeautifulSoup
    def getSoup(self, query_url):
        req = request.Request(query_url, headers=self.head)
        webpage = request.urlopen(req)
        html = webpage.read()
        #soup = BeautifulSoup(html, 'html.parser')
        soup = BeautifulSoup(html, 'html5lib')
        return soup
    # end getSoup  ---------------------------------------

    def saveHtml(self, file_name, file_content):
        file_object = open(file_name, 'w')
        file_object.write(file_content)
        file_object.close()
    # end saveHtml  ---------------------------------------

    #读取分版页面，打开分页链接
    def readPageOne(self):
        #读取页面
        soup = self.getSoup(self.one_page_url)
        #总页数
        last = soup.find("a","last")
        itemSize = int(last.string)
        page_url = str(self.two_page_url)

        #循环打开分页链接，读取分页页面
        for item in range(itemSize):
            page = str(item+1)
            new_page_url = page_url.replace( "?",page )
            print('第', page, '页---',new_page_url)
            path = self.folder_path
            self.createFolder( path)
            self.readPageTwo(new_page_url,path)

    # end readPageOne  ---------------------------------------

    #读取分页页面
    def readPageTwo(self,page_url,path):
        soup = self.getSoup(page_url)
        #first div[id="newscontent"]->div[class="l"]
        con_div = soup.find('div',{'id':'newscontent'}).find('div',{'class':'l'})
        #first div[id="newscontent"]->div[class="l"]->all spann[class="s2"]
        span_list = con_div.find_all('span',{'class':'s2'})

        #遍历span
        for span in span_list:
            #找到父节点下的span[class="s5"]，以作者为文件夹名字
            author = span.parent.find('span',{'class':'s5'}).get_text()

            #span[class="s2"]->a
            a_href = span.find('a')
            href = a_href.get('href') # 单部作品链接
            folder_name = a_href.get_text() # 作品名字
            print('a_href',href,'---folder_name',folder_name)
            new_path =  path + '\\' + author + '\\' + folder_name
            self.createFolder(new_path) # 创建文件夹
            self.readPageThree(href,new_path) # 读取单部作品

            #t = threading.Thread(target=self.readPageThree, args={href, new_path})
            #self.threads.append(t)
            # end for
     # end readPage  ---------------------------------------

    #打开作品链接，遍历单章
    def readPageThree(self,page_url,path):
        soup = self.getSoup(page_url) # 作品页面
        print('readPageThree--',page_url)
        a_list = soup.find('div', {'id': 'list'}).find_all('a')
        idx = 0 # 序号
        for a_href in a_list:
            idx = idx+1
            href = self.index_page_url +  a_href.get('href')
            txt_name =   path + '\\' +  str(idx) + '_'+ a_href.get_text()  + '.txt'
            print('a_href', href, '---path', txt_name)
            self.readPageFour(href,txt_name)

    # end readPageThree  ---------------------------------------


    #读取单章内容并写入
    def readPageFour(self,page_url,path):
        new_path = self.isTxt(path) # 是否存在，存在则返回'',没创建则返回合法文件名
        if new_path:
            soup = self.getSoup(page_url)
            con_div = soup.find('div', {'id': 'content'}) # 读取文本内容
            content = con_div.get_text().replace('<br/>', '\n').replace('&nbsp;', ' ')
            content = content.rstrip("& amp;rdquo;amp;& amp;ldquo;")

            self.writeTxt(new_path,content) # 写入文件
    # end readPageFour  ---------------------------------------

    def readPageHtml(self,page_url,path):
        soup = self.getSoup(page_url)
        con_div = soup.find('div', {'id': 'content'})
        content = con_div.get_text().replace('<br/>', '\n').replace('&nbsp;', ' ')


    def createFolder(self,path):
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        rstr = r"[\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_path = re.sub(rstr, "_", path)  # 替换为下划线
        isExists = os.path.exists(new_path)
        # 不存在则创建
        if not isExists:
            os.makedirs(new_path)
            print('目录:',new_path + ' create')
        else:
            print( new_path + ' 目录已存在')
    # end createFolder  ---------------------------------------

    def isTxt(self,path):
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        rstr = r"[\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_path = re.sub(rstr, "_", path)  # 替换为下划线
        isExists = os.path.exists(new_path)
        if isExists:
            print(new_path,'已存在')
            return ''
        else:
            return new_path
    #end createTxt ---------------------------------------

    def writeTxt(self,file_name,content):
        isExists = os.path.exists(file_name)
        if isExists:
            print(file_name,'已存在')
        else:
            file_object = open(file_name, 'w',encoding='utf-8')
            file_object.write(content)
            file_object.close()
    #end writeTxt ------------------------------------------

    def run(self):
        try:
            self.readPageOne()
        except BaseException as error:
            print('error--',error)

    def runTest(self):
        try:
            page_url = 'http://www.cuiweijuxs.com/4_4508/'
            path = '小说/runTest'
            self.readPageThree(page_url,path)
        except BaseException as error:
            print('error--',error)



Capture().run()