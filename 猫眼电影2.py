import requests
import time
from prettytable import PrettyTable#打印数据比较美观
import re
from bs4 import BeautifulSoup

def GetHTML(url):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0"}
    try:
        r = requests.get(url,headers = headers,timeout=30)
        print(r.status_code)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"

def DataClear(txt):
    print(txt)
    b = []
    soup = BeautifulSoup(txt,'html5lib')
    a = soup.find_all("dd")
    for i in a:
        c = []
        c.append(re.findall("board-index-.*?\">(.*?)</i>",str(i))[0])
        c.append(re.findall("title.*?\">(.*?)</a>",str(i))[0])#名字
        c.append(re.findall("star\">(.*?)</p>",str(i),re.S)[0].replace('\n','').replace(' ','').replace('主演：',''))#主演
        f = re.findall("\"integer\">(.*?)</i>",str(i))[0]#评分
        g = re.findall("fraction\">(.*?)</i>",str(i))[0]#评分
        c.append(f+g)#评分
        c.append(re.findall("releasetime\">(.*?)</p>",str(i))[0].replace('上映时间：',''))#上映时间
        b.append(c)
    return b
#排名，电影名称，主演，评分,上映时间

def main():
    b = []
    global url
    for i in range(0,100,10):
        a = GetHTML(url+str(i))
        print(url+str(i))
        b += DataClear(a)
    x = PrettyTable(["排名","名称","主演","评分","上映时间(地点)"])
    for i in b:
        x.add_row(i)
    return print(x)

if __name__ == '__main__':
    url = 'https://maoyan.com/board/4?offset='
    t1 = time.time()
    main()
    # print(GetHTML(url+'0'))
    print("用时{0:}".format(time.time()-t1))