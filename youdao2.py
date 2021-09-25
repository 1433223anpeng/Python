from hashlib import md5
from typing import List
import requests
import random
import time
import logging
import sys
import signal

#通过超时判断是否存在标准输入

logging.basicConfig(level= logging.INFO,filename="youdao2.py.log",filemode='a',format = "%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

class Youdao():
    def __init__(self,words:str) -> None:
        logger.info("初始化类！")
        self.root_url = "https://fanyi.youdao.com/"
        self.fanyi_url = "https://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"

        self.words = words#传入待翻译数据
        self.U_A =  {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "Host":"fanyi.youdao.com",
            "Origin":"https://fanyi.youdao.com",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "Referer":"https://fanyi.youdao.com/",
            "sec-ch-ua":'Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"'
        }
        self.session = requests.Session()
        self.session.headers.update(self.U_A)
        logger.info("类初始化已完成！")

    def get_json(self) -> List:
        ts = str(time.time()).replace('.','')[0:13]#时间戳，去掉小数点，取前13位
        salt = ts + str(random.randint(0,9))#上面的时间戳，在家一位随机数

        mb =md5()
        mb.update(self.U_A["User-Agent"].encode('utf-8'))
        bv = mb.hexdigest()

        Input_tomd5 = "fanyideskweb" + self.words + salt + "Y2FYu%TNSbMCxc3t2u^XT"

        ms = md5()
        ms.update(Input_tomd5.encode('utf-8'))
        sign = ms.hexdigest()

        data = {
            "i": self.words,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "lts": ts,
            "bv": bv,
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME",
        }
        try:
            r = self.session.post(self.fanyi_url,data=data)
            logger.info(f"正在发送POST请求url：{r.url},请求包含数据：{data}")
            r.raise_for_status
            logger.info(f"请求成功 状态码：{r.status_code}")
            return r.json()["translateResult"]
        except:
            logger.error("出现异常，HTTP请求异常，或者返回数据与之前格式不同！")
            return []
    
    def get_root(self) -> None:
        try:
            r = self.session.get(self.root_url)
            logger.info(f"请求根url：{self.root_url},状态码：{r.status_code}！")
            r.raise_for_status
            logger.info(f"请求根url：{self.root_url},请求成功！")
        except:
            logger.error(f"请求根url：{self.root_url},请求失败！")

    def show_data(self,data:dict) -> None:
        logger.info("接收到翻译返回的数据(取前50位)：{}".format(str(data)[0:50]))
        if data != []:
            for i in data:
                for x in i:
                    print(x['tgt'],end='')
        else:
            logger.error("数据解析部分出现异常，请检查类里面的 show_data函数部分!")

    def main(self) -> None:
        self.get_root()#请求主页面，保持session
        self.show_data(self.get_json())

def timeout_error(*_):
        raise TimeoutError

def help():
    print("""
有道翻译爬虫，可以翻译英语······
-h      显示帮助信息
用法：

标准输入，可以在linux等系统使用.
echo "read" ｜ python3 youdao.py

普通方法。
python3 youdao.py  read
或者
python3 youdao.py  read apple banana    #这是翻译3个单词
python3 youdao.py  "Are you OK!"        #这是翻译句子，翻译句子要加引号
""")

if __name__ == "__main__":
    logger.info("参数为：",sys.argv)
    if "-h" in sys.argv:
        help()
    elif len(sys.argv) == 1:
        signal.signal(signal.SIGALRM,TimeoutError)
        signal.alarm(1)
        try:
            words = sys.stdin.read()
            signal.alarm(0)
            Youdao(words).main()
            print()#打印换行
        except TimeoutError:
            help()
            logger.error("未在1秒内读取到标准输入！超时！")
            print("读取标准输入超时！")
    elif len(sys.argv) > 1:
        for i in sys.argv[1:]:
            Youdao(i).main()
            print(' ',end='')
        print()
    else:
        pass


    '''Youdao().main()
    a = """
There are moments in life when you miss someone so much that you just want to pick them from your dreams and hug them for real! Dream what you want to dream;go where you want to go;be what you want to be,because you have only one life and one chance to do all the things you want to do.
　　May you have enough happiness to make you sweet,enough trials to make you strong,enough sorrow to keep you human,enough hope to make you happy? Always put yourself in others’shoes.If you feel that it hurts you,it probably hurts the other person, too.
　　The happiest of people don’t necessarily have the best of everything;they just make the most of everything that comes along their way.Happiness lies for those who cry,those who hurt, those who have searched,and those who have tried,for only they can appreciate the importance of people
　　who have touched their lives.Love begins with a smile,grows with a kiss and ends with a tear.The brightest future will always be based on a forgotten past, you can’t go on well in lifeuntil you let go of your past failures and heartaches.
　　When you were born,you were crying and everyone around you was smiling.Live your life so that when you die,you're the one who is smiling and everyone around you is crying.
　　Please send this message to those people who mean something to you,to those who have touched your life in one way or another,to those who make you smile when you really need it,to those that make you see the brighter side of things when you are really down,to those who you want to let them know that you appreciate their friendship.And if you don’t, don’t worry,nothing bad will happen to you,you will just miss out on the opportunity to brighten someone’s day with this message. 
"""
'''