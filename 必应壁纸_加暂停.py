from inputimeout import inputimeout,TimeoutOccurred
import requests
import threading
import re
import time
import queue

#可以暂停意义不大
class dbtop250():
    def __init__(self):
        self.control = False
        self.control2 = True
        self.Q = queue.Queue()
        self.UA = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0"}

    def seturl(self):
        for i in range(1,15):
            url = f"https://bing.ioliu.cn/?p={i}"
            self.Q.put(url)

    def stop(self):
        while self.control2:
            try:#input_pause = input("请输入continue/pause(来控制爬虫的停止与结束)").strip().lower()
                input_pause = inputimeout(prompt="请输入continue/pause(来控制爬虫的停止与结束)", timeout=3)
                if input_pause.strip().lower() == "pause" :
                    self.control = True
                else :
                    self.control = False
            except TimeoutOccurred:
                pass

    def get_data(self,j):
        while self.control2:
            if self.Q.empty() :
                break
            while self.control:
                print(f"线程{j}暂停")
                time.sleep(1)
            try:
                s = self.Q.get()
                r = requests.get(s,headers=self.UA)
                print(r.status_code)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                a = r.text
                self.clear_data(a)
                time.sleep(2)
            except:
                print("异常")
        self.control2 = False

    def clear_data(self,txt):
        if txt != '' :
            cmp_str = re.compile(r';pic=(.*?)\?images',re.S)
            item = cmp_str.findall(txt)
            for i in item:
                print(f"图片url   ：{i}")
        
    def main(self):
        self.seturl()
        threading.Thread(target=self.stop).start()
        self.get_data(1)
        for i in range(6):
            t1 = threading.Thread(target=self.get_data,args=(i,))
            t1.start()

if __name__ == "__main__":
    dbtop250().main()