import re
import time

import requests
import os
import urllib
import urllib.request
url="https://www.vmgirls.com/13172.html"
#url="https://www.vmgirls.com/3799.html"
header={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
}
'''opener = urllib.request.build_opener()
ua=("User-Agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36")
opener.addheaders = [ua]
urllib.request.install_opener(opener)
data = urllib.request.urlopen(url).read().decode("utf-8", "ignore")
print(len(data))'''
response = requests.get(url,headers=header)
print(response.request.headers)
html=response.text
'''网址解析'''
dir_name=re.findall('<h1 class="post-title h3">(.*?)</h1>',html)[-1]
print(dir_name)
if not os.path.exists(dir_name):
    os.mkdir(dir_name)
urls=re.findall('<a href=".*?" alt=".*?" title=".*?"><img src=".*?" alt="" data-src="(.*?)" data-nclazyload="true"></a>',html)
print(urls)
print(len(urls))
'''保存图片'''
try:
    for url in urls:
        #图片命名
        #time.sleep(1)
        print("正在爬取")
        file_name= url.split("/")[-1]
        response = requests.get(url,headers=header)
        with open(dir_name+"/"+file_name,"wb") as f:
            f.write(response.content)
except Exception as err:
    pass
