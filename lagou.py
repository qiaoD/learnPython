'''
Author : QD
time   : 2018/01/28

packages : requests + BeautifulSoup + WireShark
           网页抓取基本原理 + HTML解析基本原理
webSite  : www.lagou.com
info     : Python

'''



import requests
from bs4 import *

for i in range(10):
    print(i)
    mainPage = 'https://www.lagou.com/zhaopin/Python/1'
    proxies = {
        "http": "http://61.155.164.110:3128",
    }
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Host':'www.lagou.com',
        'Referer':'https://www.lagou.com/',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36'
        }
    re = requests.get(mainPage,headers = headers,proxies=proxies)
    re.encoding = 'UTF-8'
    text = re.text                  # 解析登录页
    soup = BeautifulSoup(text, "lxml")
    tags = soup.findAll('div', class_="industry")
    for tag in tags:
        print(str(tag.text).strip())


#print(text)


class lagou:

    def __init__(self):
        pass

    def pageSearch(self):
        pass
