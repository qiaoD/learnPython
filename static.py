'''

Author   : QD
time     : 2018/01/28


'''


import time
import pymysql

import sklearn
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
import matplotlib
from matplotlib import style
style.use("ggplot")

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

    tb_type       = 'tb_type'
    tb_job        = 'tb_job'
    zhfont        = matplotlib.font_manager.FontProperties(fname='simfang.ttf')


    allTypes      = []


    def __init__(self):

        self.mysqlConnect()
        if self.mysql_conn:
            self.types()
            for job in self.allTypes:
                self.education(tid=job['id'],types=job['name'])
                self.city(tid=job['id'],types=job['name'])
            #self.lang()

    def city(self,tid = -1,types = ""):
        sqlSelect = "SELECT COUNT(*) as sum,city FROM {tb_job} WHERE tid={tid} GROUP BY city ORDER BY sum DESC LIMIT 10".format(tb_job=self.tb_job,tid=tid)
        mysql_conn = self.mysql_conn
        x = []
        y = []
        with mysql_conn.cursor() as cur:
            try:
                cur.execute(sqlSelect)
                if cur.rowcount:
                    results = cur.fetchall()
                    for row in results:
                        y.append(row[0])
                        x.append(row[1])
                    width=0.5
                    xx = np.arange(len(x))
                    plt.bar(xx, y)

                    plt.title(types+'岗位统计')
                    plt.xlabel(u'城市')
                    plt.ylabel(u'岗位数量')
                    plt.xticks(xx+width/2, x, rotation=40)
                    plt.legend(property = self.zhfont)
                    plt.savefig("images/city/"+types+".png")
            except:
                self.logInfo("Unable to get the data")


    def lang(self):
        sqlSelect = "SELECT COUNT(*) as sum,b.name  FROM {tb_job} as a,{tb_type} as b WHERE a.tid=b.id GROUP BY a.tid".format(tb_job=self.tb_job,tb_type=self.tb_type)
        mysql_conn = self.mysql_conn
        x = []
        y = []
        with mysql_conn.cursor() as cur:
            try:
                cur.execute(sqlSelect)
                if cur.rowcount:
                    results = cur.fetchall()
                    for row in results:
                        y.append(row[0])
                        x.append(row[1])
                    width=0.5
                    xx = np.arange(len(x))
                    plt.bar(xx, y)

                    plt.title('岗位统计')
                    plt.xlabel(u'语言')
                    plt.ylabel(u'岗位数量')
                    plt.xticks(xx+width/2, x, rotation=40)
                    plt.legend(property = self.zhfont)
                    plt.savefig("images/语言.png")
            except:
                self.logInfo("Unable to get the data")

    def education(self,tid = -1,types = ""):
        sqlSelect = "SELECT COUNT(*) as sum,education FROM {tb_job} WHERE tid={tid} GROUP BY education ORDER BY sum DESC".format(tb_job=self.tb_job,tid=tid)
        mysql_conn = self.mysql_conn
        x = []
        y = []
        with mysql_conn.cursor() as cur:
            try:
                cur.execute(sqlSelect)
                if cur.rowcount:
                    results = cur.fetchall()
                    for row in results:
                        y.append(row[0])
                        x.append(row[1])
                    width=0.5
                    xx = np.arange(len(x))
                    plt.bar(xx, y)

                    plt.title(types+'学历统计')
                    plt.xlabel(u'学历')
                    plt.ylabel(u'岗位数量')
                    plt.xticks(xx+width/2, x, rotation=40)
                    plt.legend(property = self.zhfont)
                    plt.savefig("images/edu/"+types+".png")
            except:
                self.logInfo("Unable to get the data")


    def types(self):
        self.logInfo("get the types in tb_type...")
        mysql_conn = self.mysql_conn
        sqlSelect = "select * from tb_type"
        with mysql_conn.cursor() as cur:
            cur.execute(sqlSelect)
            self.logInfo("all types count:"+str(cur.rowcount))
            self.allTypes = [{"id":x[0],"name":x[1],"url":x[2]} for x in cur]


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



    def logInfo(self,info):
        print(info)


    def __del__(self):
            self.mysql_conn.close()


g = lagou()
