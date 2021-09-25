from concurrent.futures import ThreadPoolExecutor
from T import ThreadPoolExecutor as TP


class FF():
    def __init__(self) -> None:
        self.A =  ["周润发","周杰伦","张杰","谢霆锋","以雷霆击碎黑暗"]
        self.TP = ThreadPoolExecutor(3)
        # self.TP = TP(2)

    def func(self,name):
        for i in range(10):
            print(f"{name}------{i}")

    def f(self):
        print(11111111111111111)

    def main(self):
        self.TP.submit(self.func,self.A[0])
        self.TP.submit(self.func,self.A[1])
        self.TP.submit(self.func,self.A[2])
        self.TP.submit(self.func,self.A[3])
        self.TP.submit(self.func,self.A[4])
        

if __name__ == "__main__":
    FF().main()