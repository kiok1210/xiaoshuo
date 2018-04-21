# -*- coding: UTF-8 -*-
from urllib import request


class Capture:

    def __init__(self):
        # 定义抓取网址
        self.init_url = 'http://www.cuiweijuxs.com/jingpinxiaoshuo/'
        # 定义headers
        self.head = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'}


    def readHtml(self):
        # 以CSDN为例，CSDN不更改User Agent是无法访问的
        # 创建Request对象
        print(self.init_url)
        req = request.Request(self.init_url, headers=self.head)
        # 传入创建好的Request对象
        response = request.urlopen(req)
        # 读取响应信息并解码
        html = response.read().decode('GBK')
        # 打印信息
        print(html)
        return html

    def saveHtml(self, file_name, file_content):
        file_object = open(file_name, 'w', encoding='utf-8')
        file_object.write(file_content)
        file_object.close()

    def run(self):
        try:
            html = self.readHtml()
            self.saveHtml('test.html', html)
        except BaseException as error:
            print(error)


Capture().run()
