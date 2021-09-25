from heapq import heappop,heappush
import threading
import time
import queue


class BPQ():
    def __init__(self,maxsize =0) -> None:#maxsize =0是队列是不会满的那种
        self._queue =[]
        self._maxsize = maxsize
        self._count = 0
        self._lock = threading.Lock()
        self._not_full = threading.Condition(self._lock)  # keep a waiting pool
        self._not_empty = threading.Condition(self._lock)  # keep a different waiting pool

    def get(self,block=True, timeout=None):
        with self._not_empty:
            if not block:#block == False时执行
                if self._count >= self._maxsize:
                    raise Exception("the unblocked queue is full, so not callable put() method!")
            else:
                if timeout is not None:
                    timeout = float(timeout)
                    if timeout < 0.0:
                        raise ValueError("timeout be should greater than zero!")
                    else:
                        last_time = time.time() + timeout
                        while self._count <= 0:
                            retime = last_time - time.time()
                            if retime <= 0:
                                raise Exception("wait time of get() operation is out of expectation")
                            self._not_empty.wait(timeout = retime)
                else:
                    while self._count <=0:
                        self._not_empty.wait()

            item = heappop(self._queue)[-1]
            self._count -=1
            self._not_full.notify(n=1)
            return item
        
    def put(self,item,priority = 0,block = True, timeout = None):#优先级设置为-45 ～ 45  （91个等级）优先级是小的先出队
        with self._not_full:
            if type(priority) is not int :
                priority = 0
            elif priority > 45:
                priority = 45
            elif priority < -45:
                priority = -45
            #确定了优先级
            if not block:
                if self._maxsize != 0 and self._count >= self._maxsize:
                    raise Exception("the unblocked queue is full, so not callable put() method!")
            else:
                if timeout is not None:
                    timeout = float(timeout)
                    if timeout < 0.0:
                        raise ValueError("timeout be should greater than zero!")
                    else:
                        last_time = time.time() + timeout
                        while self._maxsize != 0 and self._count >= self._maxsize:
                            retime = last_time - time.time()
                            if retime <= 0:
                                raise Exception("wait time of get() operation is out of expectation")
                            self._not_full.wait(timeout = retime)
                else:
                    while self._maxsize != 0 and self._count >= self._maxsize:
                        self._not_full.wait()

            print(item)
            heappush(self._queue, (priority, item))
            self._count += 1
            self._not_empty.notify(n=1)

    def qsize(self) -> int:
        with self._lock:
            return len(self._queue)

    def get_mowait(self):
        return self.get(block=False)
    
    def put_nowait(self,item,priority = 0):
        return self.put(item,priority=priority,block=False)

    def __str__(self) -> str:
        return str([i[-1] for i in self._queue])


