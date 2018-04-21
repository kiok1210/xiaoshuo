# -*- coding: UTF-8 -*-
from urllib import request
from bs4 import BeautifulSoup
import os

'''
使用BeautifulSoup抓取网页
'''

class Capture():

    def __init__(self):
        self.index_page_url = 'http://www.cuiweijuxs.com/'
        self.one_page_url = 'http://www.cuiweijuxs.com/jingpinxiaoshuo/'
        self.two_page_url = "http://www.cuiweijuxs.com/jingpinxiaoshuo/5_?.html"
        self.folder_path = '小说/'
        self.head = {}
        # 写入User Agent信息
        self.head[
            'User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'

    # 获取BeautifulSoup
    def getSoup(self, query_url):
        req = request.Request(query_url, headers=self.head)
        webpage = request.urlopen(req)
        html = webpage.read()
        #soup = BeautifulSoup(html, 'html.parser')
        soup = BeautifulSoup(html, 'html5lib')
        return soup
        # end getSoup

    # 读取更新列表
    def readPageOne(self):
        soup = self.getSoup(self.one_page_url)
        last = soup.find("a","last")
        itemSize = int(last.string)
        page_url = str(self.two_page_url)

        for item in range(itemSize):
            print( item )
            new_page_url = page_url.replace( "?",str(item+1) )
            self.readPageTwo(new_page_url)

    # end readPageOne

    #读取单页链接
    def readPageTwo(self,page_url):
        soup = self.getSoup(page_url)
        con_div = soup.find('div',{'id':'newscontent'}).find('div',{'class':'l'})
        a_list = con_div.find_all('span',{'class':'s2'})[0].find_all('a')
        print(a_list)
        for a_href in a_list:
            #print(child)
            href = a_href.get('href')
            folder_name = a_href.get_text()
            print('a_href',href,'---folder_name',folder_name)
            path = self.folder_path + folder_name
            self.createFolder(path)
            self.readPageThree(href,path)
            # end for

    # end readPageTwo

    #打开作品页面
    def readPageThree(self,page_url,path):
        soup = self.getSoup(page_url)
        print('readPageThree--',page_url)
        a_list = soup.find('div', {'id': 'list'}).find_all('a')
        idx = 0
        for a_href in a_list:
            idx = idx+1
            href = self.index_page_url +  a_href.get('href')
            txt_name =   path + '/' +  str(idx) + '_'+ a_href.get_text()  + '.txt'
            print('a_href', href, '---path', txt_name)
            isExists = os.path.exists(txt_name)
            if isExists:
                print(txt_name, '已存在')
            else:
                self.readPageFour(href,txt_name)


    #读取单章内容并写入
    def readPageFour(self,page_url,path):
        soup = self.getSoup(page_url)
        con_div = soup.find('div', {'id': 'content'})
        content = con_div.get_text().replace('<br/>', '\n').replace('&nbsp;', ' ')
        self.writeTxt(path,content)

    def readPageHtml(self,page_url,path):
        soup = self.getSoup(page_url)
        con_div = soup.find('div', {'id': 'content'})
        content = con_div.get_text().replace('<br/>', '\n').replace('&nbsp;', ' ')


    def createFolder(self,path):
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        # 不存在则创建
        if not isExists:
            os.makedirs(path)
            print(path + ' create')
        else:
            print( path + ' 目录已存在')
        #end createFolder

    def writeTxt(self,file_name,content):
        isExists = os.path.exists(file_name)
        if isExists:
            print(file_name,'已存在')
        else:
            file_object = open(file_name, 'w',encoding='utf-8')
            file_object.write(content)
            file_object.close()

    def run(self):
        try:
            self.readPageOne()
        except BaseException as error:
            print('error--',error)


Capture().run()