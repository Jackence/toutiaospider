#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import re
import time as ti
import random
import MySQLdb
import urllib2
import json
import sys



headers={
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Language":"zh-CN,zh;q=0.8",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"DNT":"1",
"Host":"www.toutiao.com",
"Referer":"http://www.toutiao.com/",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2859.0 Safari/537.36",
'Cookie':'''uuid="w:614ec9b576e2486296455e56f9435f8a"; tt_webid=43691403081; Toutiao_login_msg=1; sso_login_status=0; cp=585CB9455F819E1; __utma=24953151.642031197.1482400804.1482411887.1482469529.3; __utmc=24953151; __utmz=24953151.1482402064.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); page_referer=www.toutiao.com; _gat=1; csrftoken=c1d07e7ff7ea896046afe753ca19f0ca; utm_source=toutiao; CNZZDATA1259612802=1712019004-1482400446-%7C1482472496; __tasessionId=3vo5s9ys61482471325227; _ga=GA1.2.642031197.1482400804'''
}


def mysql(sql):
    db = MySQLdb.connect("localhost","root","","mydata" )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 设置编码UTF8
    cursor.execute('SET NAMES UTF8')
    try:
       # 执行sql语句
       cursor.execute(sql)
       # 提交到数据库执行
       db.commit()
    except:
       # 发生错误时回滚
       db.rollback()
       print sql
       print 'excute this sql error...'
       return 0
    # 关闭数据库连接
    db.close()

def getart(url,comments,id1):
    ti.sleep(3)
    ar=''
    success=0
    req=urllib2.Request(url,headers=headers)
    try:
        html1=urllib2.urlopen(req).read()
    except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
        print "The server couldn't fulfill the request"
        print "Error code:",e.code
        print "Return content:",e.read()
    except urllib2.URLError,e:
        print "Failed to reach the server"
        print "The reason:",e.reason
    else:
        soup=bs(html1,"html.parser")
        art=soup.find_all('p')
        for i in range(len(art)):
            ar1=art[i].get_text()
            ar=ar+ar1
            artcontent=ar.encode("utf-8")
            #内容
        title=soup.find('h1',class_="article-title")
        if(title):
            tix1=title.get_text().strip().encode("utf-8")
            #print tix1 #标题
            success+=1
        author=soup.find("span",class_="src")
        if(author):
            author1=author.get_text().strip().encode("utf-8")
            #print author1 #作者
            success+=1
        times=soup.find("span",class_="time")
        if(times):
            time1=times.get_text().strip().encode("utf-8")
            success+=1
            # print time1  #时间
        comments=str(comments)
        id1=urlar+id1.encode('utf-8')
        if (success==3):
            sql="INSERT INTO `entertainment`(`title`,`time`,`author`,`link`,`commenttimes`)VALUES('%s','%s','%s','%s','%s')" %(tix1,time1,author1,id1,comments)
            mysql(sql)




def getjson(url):
    ti.sleep(5)
    req=urllib2.Request(url,headers=headers)
    jscon=urllib2.urlopen(req).read()
    #print jscon
    #print "1111"
    js=json.loads(jscon)
    data=js['data']
    ne=str(js['next']['max_behot_time'])
    #print  type(ne)
    #print ne
    for i in range(len(data)-1):
        #print len(data)
        info=data[i+1]
       # print info
        try:
            comments=info['comments_count']
        except Exception, e:
            print "info['comments_count'] not find ..."
        else:
            if(comments>1000):
                #print i
                id1=data[i+1]['group_id']
                # print id1
                #print comments
                urlart=urlar+str(id1)
                getart(urlart,comments,id1)
                print "find data ..."



    url='http://www.toutiao.com/api/pc/feed/?category=news_entertainment&utm_source=toutiao&widen=1&max_behot_time='+str(ne)
    getjson(url)







urlar='http://www.toutiao.com/a'
url="http://www.toutiao.com/api/pc/feed/?category=news_entertainment&utm_source=toutiao&widen=1&max_behot_time=1490310236"


getjson(url)











