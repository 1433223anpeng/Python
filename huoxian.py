from m3u8async import wbdyM3U8
import requests
import re

url = "http://www.wbdy.tv/play/43761_1_1.html"

U_A = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        }

r = requests.get(url,headers=U_A)
a = r.text
x = re.findall('.*?url=(https://.*?index.m3u8)&id=43761&num=1&count=1&vt=1" allo.*?',a)[0]

y = requests.get(x,headers=U_A)
b = y.text
# print(b)
wbdyM3U8(b,"寂静之地.mp4").main()
