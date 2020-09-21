import re
import urllib
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
cid="6389660581532229230"
for i in range(0,100):
    url = "https://video.coral.qq.com/varticle/2461939412/comment/v2?callback=_varticle2461939412commentv2&orinum=10&oriorder=o&pageflag=1&cursor=" + str(cid) + "&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=132&_=1583316835774"
    print("第"+str(i+1)+"页的评论数据")
    data=urllib.request.urlopen(url).read().decode("utf-8","ignore")
    pat='"content":"(.*?)"'
    comments=re.compile(pat,re.S).findall(data)
    for item in comments:
        print(str(item))
        print("-------")
    cid=re.compile('"last":"(.*?)"',re.S).findall(data)[0]
