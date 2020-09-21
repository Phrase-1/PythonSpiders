import re
import urllib
import urllib.request
import requests
import os
import time
import random
import pymysql
#b站的视频号改版为BV，故20年3月25日修改了两处 av->BV  还需修改api接口的网址
def GetPageNum(response):
    all_page=1
    pat1='<li class="page-item last"><button class="pagination-btn">(.*?)</button></li>'
    max_page=re.compile(pat1,re.S).findall(response.text)
    if len(max_page):
        all_page=int(max_page[0])
    else:
        pat2='<li class="page-item"><button class="pagination-btn num-btn">(.*?)</button></li>'
        max_page=re.compile(pat2,re.S).findall(response.text)
        if len(max_page):
            all_page=int(max_page[-1])
        '''else:
            pat3='<li class="page-item"><button class="pagination-btn num-btn">(.*?)</button></li>'
            max_page=re.compile(pat3,re.S).findall(response.text)
            print(max_page[0])
            if len(max_page):
                all_page=int(max_page[0])'''
            #else:
    return all_page
def connDB():
    conn = pymysql.connect(host='localhost', user='root', passwd='WWWangenei1998!@#', db='WWW', charset='utf8')
    cur = conn.cursor()
    return (conn, cur)
def exeUpdate(conn,cur,sql):
    sta=cur.execute(sql)
    conn.commit()
    return(sta)
def exeQuery(cur,sql):
    #查询语句
    cur.execute(sql)
    result = cur.fetchone()
    return (result)
def connClose(conn,cur):
    #关闭所有连接
    cur.close()
    conn.close()

keyword=input("输入搜索关键词：")
url="https://search.bilibili.com/all"
params={
    "keyword": keyword,
    "order":"click",
    "page": 1
}
header={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
}
response=requests.get(url,headers=header,params=params)
#print(response.text)
all_page=GetPageNum(response=response)
print("一共"+str(all_page)+"页")
for curr_page in range(0,all_page):
    paramsS={
        "keyword": keyword,
        "order": "click",
        "page": curr_page+1,
    }
    serachResponse=requests.get(url,paramsS)
    pat1='<li class="video-item matrix"><a href="//www.bilibili.com/video/BV(.*?)\?from=search" title="'#问号前的转义符问题
    avSNs=re.compile(pat1,re.S).findall(serachResponse.text)
    if len(avSNs)==0:
        print("没有搜索到相关视频")
        os._exit()#结束本程序
    conn = pymysql.connect(host='localhost', user='root', passwd='WWWangenei1998!@#', db='WWW', charset='utf8')
    cursor = conn.cursor()
    print("正在爬第"+str(curr_page+1)+"页")
    print("---------------------------------")
    for avSN in avSNs:
        try:
            videoUrl="https://www.bilibili.com/video/BV"+str(avSN)
            videoResponse=requests.get(videoUrl)
            vtitle=str(re.compile('<meta data-vue-meta="true" itemprop="name" name="title" content="(.*?)_哔哩哔哩 \(゜-゜\)つロ 干杯~-bilibili">',re.S).findall(videoResponse.text)[0])
            upName=str(re.compile('<a.*?report-id="name".*?">(.*?)</a>',re.S).findall(videoResponse.text)[0])
            uploadDate=str(re.compile('<meta data-vue-meta="true" itemprop="uploadDate" content="(.*?)">',re.S).findall(videoResponse.text)[0])#需要验证关键字在不同网页的唯一性，尝试将结果转为time变量
            upId=str(re.compile('<a href="//message.bilibili.com/#whisper/mid(.*?)" target="_blank" class="message">',re.S).findall(videoResponse.text)[0])
            print(vtitle)
            #print(uploadDate)
            #print(upId)
            apiUrl="https://api.bilibili.com/x/web-interface/archive/stat"
            apiParams={"aid": str(avSN)}
            #print(apiParams)
            apiResponse=requests.get(apiUrl,headers=header,params=apiParams)
            #print(apiResponse.text)
            view=int(re.compile('"view":(.*?),',re.S).findall(apiResponse.text)[0])
            danmaku=int(re.compile('"danmaku":(.*?),',re.S).findall(apiResponse.text)[0])
            reply=int(re.compile('"reply":(.*?),',re.S).findall(apiResponse.text)[0])

            '''以下为入库操作'''
            connDB()
            sql="insert into biliinfo(keyword,vtitle,avnum,upname,upid,view,danmaku,reply,uploaddate)values"
            sql1=sql+"('"+keyword+"',"+"'"+vtitle+"',"+"'"+avSN+"','"+upName+"','"+upId+"',"+str(view)+","+str(danmaku)+","+str(reply)+",'"+uploadDate+"')"+" ON DUPLICATE KEY UPDATE view="+str(view)+",danmaku="+str(danmaku)+",reply="+str(reply)
            cursor.execute(sql1)
            conn.commit()
        except Exception  as err:
            pass
    conn.close()


