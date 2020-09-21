'''
1.分析网址，搞清网站的运作方式是get、post、还是动态加载
2.分析关键参数
3.如需抓包得到异步加载的信息，包的检索优先顺序是json>js>源码
'''
import re
import urllib
import urllib.request
import requests
import os
import time
import random
import cookiejar
keyword=input("输入你想搜索的商品：")
page=1
url="https://s.taobao.com/search?q="+keyword+"+-%E5%A4%A9%E7%8C%AB&s="+str(44*(page-1))
'''
uapools=[
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36"
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36"
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36"
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36"
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36"
]
def ua():
    opener = urllib.request.build_opener()
    thisua = random.choice(uapools)
    ua=("User-Agent",thisua)
    opener.addheaders = [ua]
    urllib.request.install_opener(opener)
    print("当前使用UA："+str(thisua))

ua()
data=urllib.request.urlopen(url).read().decode("utf-8","ignore")
#print(data)
'''
hd={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
rst=requests.get(url,headers=hd)
count=requests.get("https://rate.taobao.com/detailCount.do?_ksTS=1583637272539_116&callback=jsonp117&itemId=611105086191",cookies=rst.cookies)
print(count.text)
