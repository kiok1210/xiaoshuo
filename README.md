小说下载器
---


### install

    
    git clone github.com/kiok1210/xiaoshuo.git
    
 ### setup
 
    cd xsxz
    
    python3 ./xiaoshuo_0.6.py

### 如果不能运行,是因为引用了request、BeautifulSoup

        from urllib import request
        from bs4 import BeautifulSoup
        
### 请安装
   
    pip3 install request
   
    pip3 install BeautifulSoup
 

### 目标网站 cuiweijuxs.com

分版小说下载

> 初始化参数，下面是默认参数

        self.index_page_url = 'http://www.cuiweijuxs.com/'
        self.one_page_url = 'http://www.cuiweijuxs.com/jingpinxiaoshuo/'
        self.two_page_url = "http://www.cuiweijuxs.com/jingpinxiaoshuo/5_?.html"
        
self.one_page_url 是分版url，不下载这个，也可自行设置

这是下载后的部分内容
![看我](https://images2018.cnblogs.com/blog/1349401/201804/1349401-20180421223248272-9060498.jpg)           
    
