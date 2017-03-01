#!/usr/bin/env python
# coding=utf-8

import sys
import time
import signal
import multiprocessing
from socket import error as SocketError
from xmlrpclib import ServerProxy

from SimpleXMLRPCServer import SimpleXMLRPCServer

def add(x,y):
    return x+y

def subtract(x, y):
    return x-y

def multiply(x, y):
    return x*y

def divide(x, y):
    return x/y


# server task register
def xmlrpc_task(server=None):
    def _decorator(fn):
        if server is not None:
            server.register_function(fn, fn.__name__)

        else:
            raise Exception('Cannot find server')
        def wrapper():
            fn()

        return wrapper


class BDFWXmlRPCServer(object):
    def __init__(self):
        super(BDFWXmlRPCServer, self).__init__()
        self.data = None
        self._sdata = dict()
        self.running = True

        self.server = SimpleXMLRPCServer(("localhost", 18000), allow_none=True)
        self.server.timeout = 0.1
        self.server.register_function(self.update_data, 'update_data')
        self.server.register_function(self.set_data, 'set_data')
        self.server.register_function(self.get_data, 'get_data')
        self.server.register_function(self.stop_monitor, 'stop_monitor')
        pass

    def sighandler(self, v1, v2):
        print 'get TERM signal'
        self.stop_monitor()
        # self.server.server_close()

    def start_monitor(self):
        signal.signal(signal.SIGTERM, self.sighandler)
        # self.server.serve_forever()
        self.serve_forever()
        print 'exit xmlrpc_task'

    def serve_forever(self):
        # while self.running: self.server.handle_request()
        while 1:
            if not self.running: break
            self.server.handle_request()
        self.server.server_close()


    def stop_monitor(self):
        self.running = False
        # print dir(self.server)
        # self.server.shutdown()
        # self.server.server_close()

    def update_data(self):
        if self.data is None:
            self.data = dict()

        else:
            key = int(time.time())
            self.data[str(key)]= str(time.ctime())

        return 1

    def set_data(self, k, v):
        print 'set_data of key[%s]' % k
        self._sdata[k] = v


    def get_data(self, k=None):
        if k is None:
            return self._sdata

        return self._sdata.get(k, None)


if __name__ == '__main__':
    if sys.argv[1] == 'server':
        s = BDFWXmlRPCServer()
        try:
            s.start_monitor()
        except KeyboardInterrupt:
            s.stop_monitor()
    elif sys.argv[1] == 'c1':
        s = ServerProxy("http://127.0.0.1:18000", allow_none=True)
        print dir(ServerProxy)
        key = int(time.time())
        # s.set_data(str(key), str(time.ctime()))
        # s.set_data('dict', {'a':1})
        pass
    elif sys.argv[1] == 'c2':
        s = ServerProxy("http://127.0.0.1:18000", allow_none=True)
        try:
            print s.get_data('ip_status')
        except SocketError:
            print 'error'
    elif sys.argv[1] == 's1':
        xmlrpc_server = BDFWXmlRPCServer()
        p = multiprocessing.Process(target=xmlrpc_server.start_monitor)
        p.start()
        count = 0
        try:
            while 1:
                print 'server running...'
                count += 1
                if count == 3:
                    print 'timeout'
                    p.terminate()
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            print 'Stop by KeyboardInterrupt'
            pass
    pass
