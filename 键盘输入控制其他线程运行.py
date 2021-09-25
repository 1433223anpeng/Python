import time
import threading

class A():
    def __init__(self):
        self.control = True
        self.control2 = True
    
    def stop(self):
        while self.control2:
            input_pause = input("请输入continue/pause(来控制爬虫的停止与结束)").strip().lower()
            if input_pause == "continue" :
                self.control = True
            else :
                self.control = False

    def spyder(self):
        for i in range(100):
            while not self.control:
                time.sleep(1)
                pass
            print("{}".format(i))
            time.sleep(2)
        self.control2 = False
    
    def main(self):
        t1 = threading.Thread(target=self.stop)
        t1.start()
        t2 = threading.Thread(target=self.spyder)
        t2.start()

if __name__ == "__main__":
    A().main()
        


