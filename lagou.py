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

lists    : 1. requests API       : http://cn.python-requests.org/zh_CN/latest/
           2. BeautifulSoup API  : https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
           3. re API             : https://docs.python.org/3/library/re.html
           4. PyMySQL API        : https://www.tutorialspoint.com/python3/python_database_access.htm
           5. try-except         : https://www.tutorialspoint.com/python3/python_exceptions.htm
           6. file op            : https://www.tutorialspoint.com/python3/python_files_io.htm

******************************************************************
issues   : 1. pymysql API
           2. mysql charset
           3. how to use try - except

******************************************************************
database : lagou
tables   : tb_type , tb_job

tb_type  : id, name, url
            0, 机器学习, jiqixuexi
tb_job   : id, tid(id in tb_type), name, city, money, exper, education, company, field, stage
******************************************************************
## time:2018/01/30
1. create database and tables
2. get the homePage data
## time:2018/01/31
1. get the pages data ok
2. insert into db
3. log the result so I should alter the table named tb_type that add a colum "log"

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
    `money` varchar(255)  NOT NULL,
    `exper` varchar(255)  NOT NULL,
    `education` varchar(255)  NOT NULL,
    `company` varchar(255)  NOT NULL,
    `field` varchar(255)  NOT NULL,
    `stage` varchar(255)  NOT NULL,
    `url` varchar(255)  NOT NULL,
    PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin,
AUTO_INCREMENT=1;

'''


import time
import re
import requests
from bs4 import *
import pymysql

import win_unicode_console
win_unicode_console.enable()


class lagou:

    # mysql config
    mysql_host    = '127.0.0.1'
    mysql_user    = 'root'
    mysql_pwd     = 'root'
    mysql_db      = 'lagou'
    mysql_port    = 3306
    mysql_conn    = 0
    mysql_charset = 'utf8'

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
    writeUrl  = 'html/'


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
                                   charset  = self.mysql_charset
                                  )
        except:
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
        self.logInfo("beginning...")
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
            #print(sqlInsert)
            self.logInfo("insert into mysql...")
            with mysql_conn.cursor() as cur:
                cur.execute(sqlInsert.strip(","))
                mysql_conn.commit()

    def types(self):
        self.logInfo("get the types in tb_type...")
        mysql_conn = self.mysql_conn
        sqlSelect = "select * from tb_type"
        with mysql_conn.cursor() as cur:
            cur.execute(sqlSelect)
            self.logInfo("all types count:"+str(cur.rowcount))
            self.allTypes = [{"id":x[0],"name":x[1],"url":x[2]} for x in cur]




    def jobs(self):
        allTypes = self.allTypes
        for types in allTypes:
            self.jobInfo(types['id'],types['url'])


    def jobInfo(self,tid=-1,cat=''):
        url = self.listUrl + cat + '/'
        headers = self.headers  # http headers
        proxiesList = self.proxies  # https proxy IP
        self.logInfo("beginning get the cat:" + url)
        mysql_conn = self.mysql_conn

        pageList = [x for x in range(1,31)]
        # get the page in for loop
        while(pageList):
            if proxiesList:
                proxies = {"https":proxiesList.pop()}
            else:
                self.makeproxies()
                proxiesList = self.proxies
            pageNum = pageList[0]
            numUrl  = url + str(pageNum)

            self.logInfo("begin to get the url:"+numUrl)

            try:
                reqGet = requests.get(url = numUrl, headers = headers,proxies = proxies, timeout=5)
            except:
                self.logInfo('error!')
            else:
                print(reqGet.status_code)
                if reqGet.status_code == 404 :
                    break;
                reqGet.encoding = 'UTF-8'
                pageText = reqGet.text
                soup = BeautifulSoup(pageText, "lxml")
                tags = soup.findAll(name='li',attrs={"class":"con_list_item"})
                # name, city, lmoney, hmoney, exper, education, company, field, stage
                if tags:
                    # write in .html
                    self.logInfo("begin to write in html")
                    self.htmlWrite(pageText,cat+str(pageNum)+".html")
                    self.logInfo("end ...")
                    sqlInsert = 'insert into tb_job(`tid`,`name`,`city`,`money`,`exper`,`education`,`company`,`field`,`stage`,`url`) VALUES'
                    for tag in tags:
                        name       = tag.find(name='h3').text.strip()
                        city       = tag.find(name='em').text.split('·')[0].strip()
                        money      = tag.find(name='span',attrs={"class":"money"}).text.strip()
                        li_b       = tag.find(name='div',attrs={"class":"li_b_l"}).text
                        pos        = li_b.rfind("k")+1
                        if -1 == pos:
                            pos    = li_b.rfind("K")+1
                        experAndEd = li_b[pos:].split('/')
                        exper      = experAndEd[0].strip()
                        education  = experAndEd[1].strip()
                        company    = tag.find(name='div',attrs={"class":"company_name"}).find(name='a').text.strip()
                        industry   = tag.find(name='div',attrs={"class":"industry"}).text.split('/')
                        field      = industry[0].strip()
                        stage      = industry[1].strip()
                        sqlUrl       = tag.find(name='a',attrs={"class":"position_link"}).get('href').strip()
                        self.logInfo(name+','+city+','+money+','+exper+','+education+','+company+','+field+','+stage)
                        sqlInsert += '('+str(tid)+','+'"'+name+'","'+city+'","'+money+'","'+exper+'","'+education+'","'+company+'","'+field+'","'+stage+'","'+sqlUrl+ '"),'


                    self.logInfo("begin to write into mysql..")
                    #self.logInfo(sqlInsert)
                    with mysql_conn.cursor() as cur:
                        try:
                            cur.execute(sqlInsert.strip(","))
                            mysql_conn.commit()
                        except:
                            self.logInfo("mysql error")
                        else:
                            del(pageList[0])
                    self.logInfo("end..")


    def htmlWrite(self,text,filename):
        url = self.writeUrl+filename
        with open(url, "w", encoding='UTF-8') as f:
            f.write(text)
        f.close()

    def logInfo(self,info):
        print(info)


    def __del__(self):
            self.mysql_conn.close()


g = lagou()
