'''
Author : QD
time   : 2018/01/28

******************************************************************
packages : requests + BeautifulSoup + re + time + PyMySQL
           网页抓取基本原理 + HTML解析基本原理
           requests       : API基本函数使用 + 使用代理
           BeautifulSoup  : API + 正则表达式写法
           爬虫关键字      : 分布式 | 多线程 | 代理
webSite  : www.lagou.com
proxy web: http://www.xicidaili.com/wt/
info     : the job types + job information
******************************************************************
database : lagou
tables   : tb_type , tb_job

tb_type  : id, name, url
            0, 机器学习, jiqixuexi
tb_job   : id, tid(id in tb_type), name, city, lmoney, hmoney, exper, education, company, field, stage

'''


import time
import re
import requests
from bs4 import *
import pymysql

for i in range(1):
    #time.sleep(15)
    mainPage = 'https://www.lagou.com/'
    proxies = {
        "http": "http://114.216.253.179:8118",
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
    req = requests.get(mainPage)
    if req:
        print(i)
        #re.encoding = 'UTF-8'
        text = req.text                  # 解析登录页
        soup = BeautifulSoup(text, "lxml")
        tags = soup.findAll(name='a',attrs={"href":re.compile(r'^https://www.lagou.com/zhaopin/')})
        for tag in tags:
            print(tag.get('href').strip('/'))
            tt = tag.get('href').strip('/').split('/')[-1]
            print(str(tt))


#print(text)


class lagou:

    # spider config
    proxies = ['http://113.83.241.17:8118'

              ]
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

    # web info
    homePage   = 'https://www.lagou.com/'
    listPage   = 'https://www.lagou.com/zhaopin/'


    def __init__(self):
        pass

    # 1. get job types and links in homePage
    # 2. write into the mysql
    def homePage(self):
        pass

    def jobs(self):
        pass

    def jobInfo(self,cat=''):
        pass
