from TP import ThreadPool

x = ThreadPool(2)

def A(a):
    print(a)
    x.submit(B,"这是B",priority=0)

def B(b):
    print(b)


if __name__ =="__main__":
    x.submit(A,"这是A",priority=0)
    x.submit(B,"这是A",priority=0)
    x.submit(B,"这是A",priority=0)
    x.submit(B,"这是A",priority=0)
    x.submit(B,"这是A",priority=0)
    x.submit(B,"这是A",priority=0)
    x.submit(B,"这是A",priority=0)
    x.submit(B,"这是A",priority=0)
    x.submit(B,"这是A",priority=0)
