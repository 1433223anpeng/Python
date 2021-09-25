import requests
from hashlib import md5
import re
import sys
import signal

class SougouFanyi():
    def __init__(self,words) -> None:
        self.words = words
        self.U_A = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
        }
        self.session = requests.session()
        self.session.headers.update(self.U_A)

        self.root_url = "https://fanyi.sogou.com/"
        
        self.s_str = "auto" + "zh-CHS" + self.words
        self.api = "https://fanyi.sogou.com/api/transpc/text/result"

    def get_root(self):
        try:
            r = self.session.get(self.root_url)
            r.raise_for_status
            r.encoding = r.apparent_encoding
            return r.text
        except Exception as e:
            print(f"发生异常 在get_root函数  >>> {e}")

    def get_resu(self):
        try:
            r = self.session.post(self.api,data=self.data)
            r.raise_for_status
            return r.json()["data"]["translate"]["dit"]
        except Exception as e:
            print(f"发生异常 在get_resu函数  >>> {e}")

    def get_uuid_secretCode(self,text):
        try:
            cmp = re.compile(r'"secretCode":(?P<secretCode>\d+),"uuid":"(?P<uuid>.*?)"')
            a = cmp.search(text)
            uuid = a.group("uuid")
            secretCode = a.group("secretCode")
            return uuid,secretCode
        except:
            print("发生异常 在get_uuid_secretCode函数，未能获取uuid和secretCode")

    def m5(self,x):
        m5 = md5()
        m5.update(x.encode())
        s = m5.hexdigest()
        return s

    def main(self):
        a = self.get_root()
        uuid,secretCode = self.get_uuid_secretCode(a)
        s = self.m5(self.s_str+secretCode)
        self.data = {
                "from": "auto",
                "to": "zh-CHS",
                "text": self.words,
                "client": "pc",
                "fr": "browser_pc",
                "needQc": 1,
                "s": s,
                "uuid": uuid,
                "exchange": "false"
        }
        print(self.get_resu())

def timeout_error(*_):
        raise TimeoutError

def help():
    print("""
有道翻译爬虫，可以翻译英语······
-h      显示帮助信息
用法：

标准输入，可以在linux等系统使用.
echo "read" ｜ python3 SougouFanyi.py

普通方法。
python3 SougouFanyi.py  read
或者
python3 SougouFanyi.py  read apple banana    #这是翻译3个单词
python3 SougouFanyi.py  "Are you OK!"        #这是翻译句子，翻译句子要加引号
""")

if __name__ == "__main__":
    if "-h" in sys.argv:
        help()
    elif len(sys.argv) == 1:
        signal.signal(signal.SIGALRM,TimeoutError)
        signal.alarm(1)
        try:
            words = sys.stdin.read()
            signal.alarm(0)
            SougouFanyi(words).main()
            print()#打印换行
        except TimeoutError:
            help()
            print("读取标准输入超时！")
    elif len(sys.argv) > 1:
        for i in sys.argv[1:]:
            SougouFanyi(i).main()
            print(' ',end='')
        print()
    else:
        pass
