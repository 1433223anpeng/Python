#这个就是线程池
from concurrent.futures import ThreadPoolExecutor

from T import ThreadPoolExecutor as TP

def func(name,x):
    x.submit(fn,name)
    for i in range(10):
        print(f"{name}---{i}")
    


def fn(name):
    for i in range(10):
        print(f"{name}2---{i}")

if __name__ == "__main__":
    a = ["周润发","周杰伦","张杰","谢霆锋","以雷霆击碎黑暗"]

    with ThreadPoolExecutor() as f:#这种无法顺序处理返回值只能在submit().add_done_callback()  使用这种回调函数
        for i in a:
            f.submit(func,i,f)

    # # x = TP(10)
    # print(123)
    # with TP() as x:
    #     x.submit(func,a[0],x,priority= 5)
    #     x.submit(func,a[1],x,priority=8)
    #     x.submit(func,a[2],x,priority=33)
    #     x.submit(func,a[3],x,priority=0)
    #     x.submit(func,a[4],x,priority=0)
        

    

    # with ThreadPoolExecutor(4) as f:#这种map是由返回值的，返回一个迭代器，先传入的先返回，按顺序返回， for 循环提取,获取返回值
    #     x = f.map(func,a)
    #     for i in x:
    #         print(i)   
    print("-"*10)