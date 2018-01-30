'''

Author   : QD
time     : 2018/01/28

******************************************************************
packages : requests + BeautifulSoup + re + time + PyMySQL
           网页抓取基本原理 + HTML解析基本原理 + 正则表达式
           requests       : API基本函数使用 + 使用代理
           BeautifulSoup  : API + 正则表达式写法
           爬虫关键字      : 分布式 | 多线程 | 代理
webSite  : www.lagou.com
proxy web: http://www.xicidaili.com/wn/
info     : the job types + job information
******************************************************************
issues   : 1. pymysql API
           2. mysql charset
           3. how to use try - except

******************************************************************
database : lagou
tables   : tb_type , tb_job

tb_type  : id, name, url
            0, 机器学习, jiqixuexi
tb_job   : id, tid(id in tb_type), name, city, lmoney, hmoney, exper, education, company, field, stage
******************************************************************
## time:2018/01/29
1. create database and tables
2. get the homePage data

create database `lagou`;
use lagou;
CREATE TABLE `tb_type` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255)  NOT NULL,
    `url` varchar(255)  NOT NULL,
    PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin,
AUTO_INCREMENT=1;

CREATE TABLE `tb_job` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `tid` int(11)  NOT NULL,
    `name` varchar(255)  NOT NULL,
    `city` varchar(255)  NOT NULL,
    `lmoney` int(11)  NOT NULL,
    `hmoney` int(11)  NOT NULL,
    `exper` varchar(255)  NOT NULL,
    `education` varchar(255)  NOT NULL,
    `company` varchar(255)  NOT NULL,
    `field` varchar(255)  NOT NULL,
    `stage` varchar(255)  NOT NULL,
    PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin,
AUTO_INCREMENT=1;

'''


import time
import re
import requests
from bs4 import *
import pymysql
'''
for i in range(1):
    #time.sleep(15)
    mainPage = 'https://www.lagou.com/'
    proxies = {
        "https": "119.129.98.11:9797",
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
    try:
        req = requests.get(mainPage, proxies = proxies)
    except requests.exceptions.ProxyError:
        print('error')
    else:
        print(i)
        #re.encoding = 'UTF-8'
        text = req.text                  # 解析登录页
        soup = BeautifulSoup(text, "lxml")
        tags = soup.findAll(name='a',attrs={"href":re.compile(r'^https://www.lagou.com/zhaopin/.')})
        for tag in tags:
            print(tag.get('href').strip('/'))
            tt = tag.get('href').strip('/').split('/')[-1]
            print(str(tt))


#print(text)
'''

class lagou:

    # mysql config
    mysql_host    = '127.0.0.1'
    mysql_user    = 'root'
    mysql_pwd     = 'root'
    mysql_db      = 'lagou'
    mysql_port    = 3306
    mysql_conn    = 0

    # spider config
    proxyUrl      = 'http://tvp.daxiangdaili.com/ip/?tid=559934516929845&num=1000&delay=1&protocol=https'
    proxies       = []
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
    homeUrl   = 'https://www.lagou.com/'
    listUrl   = 'https://www.lagou.com/zhaopin/'
    allTypes  = []


    def __init__(self):

        self.mysqlConnect()
        if self.mysql_conn:
            # self.homePage()     # get the homePage
            self.types()

            self.makeproxies()
            self.jobs()

    def makeproxies(self):
        url = self.proxyUrl
        reqGet = requests.get(url)
        self.proxies = reqGet.text.split("\r\n")


    def mysqlConnect(self):
        try:
            conn = pymysql.connect(host     = self.mysql_host,
                                   user     = self.mysql_user,
                                   password = self.mysql_pwd,
                                   db       = self.mysql_db,
                                   port     = self.mysql_port,
                                   charset  = "utf8"
                                  )
        except pymysql.err.OperationalError:
            print("link mysql error!")
        else:
            self.mysql_conn = conn
            #print("link seccuess")


    # 1. get job types and links in homePage
    # 2. write into the mysql
    def homePage(self):
        # sql
        mysql_conn = self.mysql_conn
        sqlInsert = "insert into tb_type(`name`,`url`) VALUES "
        print("beginning...")
        req = requests.get(self.homeUrl)
        if req.status_code == 200:
            req.encoding = 'UTF-8'
            text = req.text
            soup = BeautifulSoup(text, "lxml")
            tags = soup.findAll(name='a',attrs={"href":re.compile(r'^https://www.lagou.com/zhaopin/.')})
            for tag in tags:
                name = str(tag.text).strip()
                url = tag.get('href').strip('/').split('/')[-1]
                print(name+"--"+url)
                sqlInsert += '("'+name+'","'+url+'"),'
            print(sqlInsert)
            print("insert into mysql...")
            with mysql_conn.cursor() as cur:
                cur.execute(sqlInsert.strip(","))
                mysql_conn.commit()

    def types(self):
        print("get the types in tb_type...")
        mysql_conn = self.mysql_conn
        sqlSelect = "select * from tb_type"
        with mysql_conn.cursor() as cur:
            cur.execute(sqlSelect)
            print("all types count:"+str(cur.rowcount))
            self.allTypes = [{"name":x[1],"url":x[2]} for x in cur]




    def jobs(self):
        allTypes = self.allTypes
        for types in allTypes:
            self.jobInfo(types['url'])


    def jobInfo(self,cat=''):
        url = self.listUrl + cat + '/'
        headers = self.headers  # http headers
        proxiesList = self.proxies  # https proxy IP
        print("beginning get the cat:" + url)

        pageList = [x for x in range(1,31)]
        print(pageList)
        # get the page in for loop
        while(pageList):
            if proxiesList:
                proxies = {"https":proxiesList.pop()}
            else:
                self.makeproxies()
                proxiesList = self.proxies
            print(proxies)
            pageNum = pageList[0]
            try:
                reqGet = requests.get(url = url + str(pageNum), headers = headers,proxies = proxies, timeout=5)
            except:
                print('error')
            else:
                if reqGet.status_code == 400:
                    break;
                reqGet.encoding = 'UTF-8'
                pageText = reqGet.text
                soup = BeautifulSoup(pageText, "lxml")
                tags = soup.findAll(name='li',attrs={"class":"con_list_item"})
                # name, city, lmoney, hmoney, exper, education, company, field, stage
                for tag in tags:
                    name = tag.find(name='h3').text
                    city = tag.find(name='em').text.split('·')[0].strip()
                    moneys = tag.find(name='span',attrs={"class":"money"}).text.split('-')
                    print(pageNum)
                del(pageList[0])



    def __del__(self):
            self.mysql_conn.close()


g = lagou()
