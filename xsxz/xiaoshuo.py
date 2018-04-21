from urllib import request
import chardet


if __name__ == "__main__":
    chaper_url = "http://www.cuiweijuxs.com/jingpinxiaoshuo/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = request.Request(url=chaper_url, headers=headers)
    response = request.urlopen(req)
    html = response.read()
    print(html)

    # 查看网页编码格式
    charset = chardet.detect(html)
    print(charset)

    # 查看网页内容
    #try:
    html = html.decode('GBK')
    #except:
    #    html = html.decode('utf-8')
    print(html)
    



'''
#获取request python2可以直接使用urllib2
request =  urllib.request
 
# 直接请求
response = request.urlopen('http://www.baidu.com')
 
# 获取状态码，如果是200表示获取成功
print( response.getcode() )
 
# 读取内容
cont = response.read()
'''
