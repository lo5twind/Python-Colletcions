#!/usr/bin/env python
# coding=utf-8

import time
from multiprocessing import Pool,Queue,Manager


class MP(object):
    def __init__(self):
        super(MP,self).__init__()
        self.MAX = 4

        pass

    def go_to_work(self):
        manager = Manager()
        q = manager.Queue()
        pool = Pool()
        for i in range(self.MAX):
            pool.apply_async(worker,args=(i,q,))
        for i in range(10):
            q.put(i)
            time.sleep(1)
        for _ in range(self.MAX):
            q.put('quit')

def worker(n,q):
    while 1:
        print 'worker[%s] waiting...' % n
        item = q.get()
        print 'worker[%s] get [%s]...' % (n,item)
        print item
        if item == 'quit':
            break
    print 'worker[%s] exit...' % n

def consumer(n,q):

    while 1:
        print 'consumer[%s] waiting...' % n
        item.put(counter)

if __name__ == '__main__':
    import threading
    value = ['beginValue']
    MP().go_to_work()
    value.append('secondValue')
    print 'here????????????'
    print 'here????????????'
    print 'here????????????'
    print 'here????????????'
    pass
