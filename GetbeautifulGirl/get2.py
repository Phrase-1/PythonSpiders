import re
import urllib
import urllib.request
import time
import os
import random
import requests
'''本程序用以爬取http://www.meitucha.com/网站的图片，使用时进入摄影集页面，确定页数，修改allPage的值，再修改urlid的值即可；
目标网站有反爬策略，用时可搭配ua池和vpn'''
page=1
#allPage=4
urlid=32305
url="http://www.meitucha.com/a/"+str(urlid)+"/?page="+str(page)
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
'''UA=("User-Agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36")
opener=urllib.request.build_opener()
opener.addheaders=[UA]
urllib.request.install_opener(opener)'''
data=urllib.request.urlopen(url).read().decode("utf-8","ignore")
dir_name=re.compile("<h1>(.*?)</h1>",re.S).findall(data)[0]
if not os.path.exists(dir_name):
    os.mkdir(dir_name)
allImg=int(re.compile('<p>图片数量： (.*?)P</p>',re.S).findall(data)[0])
allPage=allImg//5+1
for i in range(0,allPage):
    print("正在爬第"+str(i+1)+"页图片")
    data=urllib.request.urlopen(url).read().decode("utf-8","ignore")
    pat='<img src="(http.*?)" alt=".*?" class=".*?">'
    urls=re.compile(pat,re.S).findall(data)
    print(urls)
    for url in urls:
        img = urllib.request.urlopen(url).read()
        file_name=url.split("/")[-1]
        with open(dir_name+"/"+file_name,"wb") as f:
            f.write(img)
        time.sleep(1)
        ua()
    page=page+1
    url = "http://www.meitucha.com/a/"+str(urlid)+"/?page=" + str(page)
    time.sleep(1)

