#写个优先级队列
import threading

try:
    from _queue import Empty
except ImportError:
    class Empty(Exception):
        'Exception raised by Queue.get(block=0)/get_nowait().'
        pass

class Full(Exception):
    'Exception raised by Queue.put(block=0)/put_nowait().'
    pass

class __AAA():
    def __init__(self) -> None:
        print("ok!")

class PQ():
    def __init__(self,maxsize = 0) -> None:#默认大小
        self._queue = []
        self.maxsize = maxsize
        self.mutex = threading.Lock()
        self.not_empty = threading.Condition(self.mutex)
        self.not_full = threading.Condition(self.mutex)
        self.all_tasks_done = threading.Condition(self.mutex)
        self.unfinished_tasks = 0
        self.get_nowait = self.get
        self.put_nowait = self.put

    def __str__(self) -> str:
        return str([i[-1] for i in self._queue])

    def put(self,item,priority = 90,block = True):#priority是优先级，0-90，小的优先，默认优先级最低
        if  type(priority) != int or priority > 90 :
            priority = 90
        elif priority < 0:
            priority = 0

        with self.not_full:
            if self.maxsize > 0:
                if not block:
                    if self._qsize() >= self.maxsize:
                        raise Full
                else :
                    while self._qsize() >= self.maxsize:
                        self.not_full.wait()

            self._put(item,priority)
            self.unfinished_tasks += 1
            self.not_empty.notify()
    
    def join(self):
        with self.all_tasks_done:
            while self.unfinished_tasks:
                self.all_tasks_done.wait()

    def task_done(self):
        with self.all_tasks_done:
            unfinished = self.unfinished_tasks - 1
            if unfinished <= 0:
                if unfinished < 0:
                    raise ValueError('task_done() called too many times')
                self.all_tasks_done.notify_all()
            self.unfinished_tasks = unfinished

    def get(self,block = True):
        with self.not_empty:
            if not block:
                if not self._qsize():
                    raise Empty
            else :
                while not self._qsize():
                    self.not_empty.wait()

            item = self._get()
            self.not_full.notify()
            return item
    
    def qsize(self):
        with self.mutex:
            return self._qsize()

    def empty(self):
        with self.mutex:
            return not self._qsize()

    def full(self):
        with self.mutex:
            return 0 < self.maxsize <= self._qsize()

    def _qsize(self):
        return len(self._queue)

    def _put(self, item, priority):
        self._queue.append((priority,item))
        #给他排序
        self._queue.sort(reverse = True,key = lambda x:x[0])#逆序，列表后面的元素需要先出队
        # print(self._queue)

    def _get(self):
        return self._queue.pop()[-1]