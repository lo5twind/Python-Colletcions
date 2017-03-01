#!/usr/bin/env python
# coding=utf-8

import os
import time
import signal
import psutil
import threading

# register TERM signal action, when get TERM signal raise a runtimeerror
def sighandler(var1, var2):
    print 'get signal %s' % var1
    raise RuntimeError('Get Exit Signal')

class CPUController(threading.Thread):
    def __init__(self):
        super(CPUController, self).__init__()
        self.event = threading.Event()
        self.rest_time = 0
        signal.signal(signal.SIGTERM,sighandler)


    def cpu_monitor(self, cpu_no=None, ivl=0.1):
        pre_cpu_per = 0
        while 1:
            if self.event.isSet():
                break
            if cpu_no is None:
                cpu_per = psutil.cpu_percent(interval=ivl)
            else:
                cpu_per = psutil.cpu_percent(interval=ivl, percpu=True)[cpu_no]

            print 'CPU {}% ---> {}%'.format(pre_cpu_per, cpu_per)
            pre_cpu_per = cpu_per

            pre_rest_time = self.rest_time
            if cpu_per > 20:
                self.rest_time = 100 if self.rest_time >= 100 else self.rest_time + 0.01
            elif cpu_per <= 20 and cpu_per > 10:
                self.rest_time = 0 if self.rest_time <= 0 else self.rest_time - 0.00005
            elif cpu_per <= 10 and cpu_per >= 0:
                self.rest_time = 0 if self.rest_time <= 0 else self.rest_time - 0.0001
            print 'SLT {} ---> {}'.format(pre_rest_time, self.rest_time)
            # print 'SleepTime = %s' % self.rest_time

            time.sleep(1)
            pass


    def cpu_worker(self):
        while 1:
            if self.event.isSet():
                break
            pass


    def run(self):
        print 'CPUController starts running...'
        # do something
        a = 0
        while 1:
            if self.event.isSet():
                break
            a = (a + 1) % 10000
            a = (a + 1) % 10000
            a = (a + 1) % 10000
            a = (a + 1) % 10000
            a = (a + 1) % 10000
            a = (a + 1) % 10000
            a = (a + 1) % 10000
            time.sleep(self.rest_time if self.rest_time > 0 else 0)
            # time.sleep(1)


    def stop(self):
        self.event.set()


if __name__ == '__main__':
    cc = CPUController()
    print 'CPUController started...waiting Exit signal'
    cc.start()
    try:
        cc.cpu_monitor()
    except (KeyboardInterrupt, RuntimeError) as e:
        print 'get stop signal'
        cc.stop()

    print 'CPUController stoped'
    pass
