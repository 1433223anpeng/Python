import requests
import threading
import re
import time
import queue

class MyThread(threading.Thread):
    def __init__(self,f1,f2,j,data):
        threading.Thread.__init__(self)
        self.fget = f1
        self.fclear = f2
        self.j = j
        self.data = data
    def run(self):
        while self.data.qsize()>0:
            self.fclear(self.fget(self.data,self.j))

class dbtop250():
    def __init__(self):
        self.control = False
        self.control2 = True
        self.Q = queue.Queue()
        self.UA = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0"}

    def seturl(self):
        for i in range(0,250,25):
            url = f"https://movie.douban.com/top250?start={i}&filter="
            self.Q.put(url)
            

    def stop(self):
        while self.control2:
            input_pause = input("请输入continue/pause(来控制爬虫的停止与结束)").strip().lower()
            if input_pause == "continue" :
                self.control = True
            else :
                self.control = False

    def get_data(self,j):
        print(444)
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

                
    def clear_data(self,txt):
        if txt != '' :
            print(txt)
            cmp_str = re.compile(r'<span class="title">(?P<title>.*?)</span>.*?<p class="">.*?导演: (?P<daoyan>.*?)&nbsp;',re.S)
            item = cmp_str.finditer(txt)
            for i in item:
                title = i.group('title')
                daoyan = i.group('daoyan')
                print(f"电影：{title}----导演：{daoyan}")
        
    # def run(self,i):
    #     self.get_data(i)

    def main(self):
        print(111)
        self.seturl()
        threading.Thread(target=self.stop).start()
        self.get_data(1)
        # for i in range(6):
        #     t1 = threading.Thread(target=self.get_data,args=(i,))
        #     t1.start()
        print(222)



if __name__ == "__main__":
    dbtop250().main()
    # a = [1,2,3,4,5,6,7,8,9,0]
    # Q = queue.Queue()
    # for i in range(0,250,25):
    #     # Q.put(i)
    #     print(i)
    # # while (Q.qsize()>0):
    #     print(Q.get())
        