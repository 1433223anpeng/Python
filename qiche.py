from pyquery import PyQuery
import json
import requests
from requests.models import requote_uri

def parse_html(txt):
    doc = PyQuery(txt)
    nodes = doc(".mt-10").items()
    for node in nodes:
        a = node("dl > dt").eq(2)
        if a.text() != "购车经销商":#统一化数据
            node("dl").eq(2).after(PyQuery("""<dl class="choose-dl">
                        <dt>购车经销商</dt>
                        <dd>
                            <a href="###" class="js-dearname" data-val='116803,50077' data-evalid="3605235" target="_blank">
                                &nbsp
                            </a>
                        </dd>
                    </dl>"""))
        chex = node("dl > dd").eq(0).text().replace('\n'," ")
        didian = node("dl > dd").eq(1).text()
        price = node("dl > dd").eq(4).text()
        other = node("div > div > dl").text().replace("\n",":").split(' ')
        json_D = dict()
        json_D["车型"] = chex
        json_D["购车地点"] = didian
        json_D["裸车价格"] = price
        json_D["评价"] = ','.join(other)
        a = json.dumps(json_D,ensure_ascii=False)
        with open("汽车之家.json",'a') as f:
            f.write(a+'\n')
        
def get_html(url):
    U_A = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0"}
    try:
        r = requests.get(url,headers=U_A)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("出现异常")

if __name__ == "__main__" :
    URL = "https://k.autohome.com.cn/5714/index_4.html#dataList"
    b = get_html(URL)
    parse_html(b)
    print("OK!")