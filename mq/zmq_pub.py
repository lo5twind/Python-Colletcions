#!/usr/bin/env python
# coding=utf-8


import os
import sys
import zmq
import time
import json
import copy
import threading
from contextlib import contextmanager


PUB_POTR = 5000
REP_POTR = 5001
ZMQ_ADDR = "tcp://127.0.0.1:{port:}"
ZMQ_PREFIX = r'ZMQ://'
ZMQ_MSG = lambda x : ZMQ_PREFIX + x
# ZMQ_EXIT = ZMQ_MSG("{command:'exit'}")
ZMQ_STAT = lambda ty, msg : ZMQ_MSG("{%s:'%s'}" % (ty, msg))

ZMQ_EXIT = ZMQ_STAT('command', 'exit')
ZMQ_INVALIDE_MSG = ZMQ_STAT('error', 'invalide message')


def zmq_pub():
    try:
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://127.0.0.1:5000")
        count = 0
        while 1:
            socket.send("zmq send [%s]" % count)
            count += 1
            time.sleep(1)
    except KeyboardInterrupt as e:
        print 'zmq_pub quit...'
        socket.close()
        sys.exit(e)


def zmq_server():
    try:
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://127.0.0.1:5001")
        while 1:
            msg = socket.recv()
            print 'zmq_server get msg[%s]' % msg
            socket.send(msg)

    except KeyboardInterrupt as e:
        print 'zmq_server quit...'
        socket.close()
        sys.exit(e)


@contextmanager
def zmq_pub_socket():
    try:
        pub_context = zmq.Context()
        pub_socket = pub_context.socket(zmq.PUB)
        pub_socket.bind(ZMQ_ADDR.format(port=PUB_POTR))
        yield pub_socket
    finally:
        print 'ZmqPubServer: pub_socket Exit'
        pub_socket.close()


@contextmanager
def zmq_rep_socket():
    try:
        rep_context = zmq.Context()
        rep_socket = rep_context.socket(zmq.REP)
        rep_socket.bind(ZMQ_ADDR.format(port=REP_POTR))
        yield rep_socket
    finally:
        rep_socket.close()
        print 'ZmqPubServer: rep_socket Exit'


class EventMonitors(object):


    def __init__(self):
        super(EventMonitors, self).__init__()
        base_attr = set(dir(EventMonitors.__class__.__mro__[-1]))
        event_attr = set(dir(EventMonitors))
        for func in base_attr ^ event_attr:
            callable_func = getattr(EventMonitors, func)
            if callable(callable_func):
                setattr(self.__class__, func.upper(), func)

    @classmethod
    def update_file_mtime(cls, file_list, res):
        for f in file_list:
            try:
                f_name = os.path.split(f)[1]
                res[f_name] = os.path.getmtime(f)
            except OSError:
                continue


    @classmethod
    def update_file_size(cls, file_list, res):
        for f in file_list:
            try:
                f_name = os.path.split(f)[1]
                res[f_name] = os.path.getsize(f)
            except OSError:
                continue


    @classmethod
    def update_table_mtime(cls, tb_list, res_list):
        pass

class ZmqPubServer(threading.Thread):

    event_monitors = set()

    def __init__(self):
        super(ZmqPubServer, self).__init__()

        self.event = threading.Event()
        self.event_monitors = {}
        self.event_queue = {}

        self.reg_event_status = {}
        self.reg_event_status_last = {}
        self.reg_event_set = set()


        base_attr = set(dir(EventMonitors.__class__.__mro__[-1]))
        event_attr = set(dir(EventMonitors))
        for func in base_attr ^ event_attr:
            callable_func = getattr(EventMonitors, func)
            if callable(callable_func):
                # setattr(self.__class__, func, callable_func)
                setattr(self.__class__, func.upper(), func)
                self.event_monitors[func] = callable_func
                self.event_queue[func] = []



    def event_add_handler(self, handler, *args, **kwargs):
        handler(*args, **kwargs)


    def event_register(self):
        with zmq_rep_socket() as rep_socket:
            while 1:
                msg = rep_socket.recv()
                print 'zmq_server get msg[%s]' % msg
                # add by a handler, wait to modify
                rep_socket.send(msg)
                if msg == ZMQ_EXIT:
                    break
                self.reg_event_set.add(msg)
                msg_d = self.zmq_message_parser(msg)
                try:
                    for event in msg_d:
                        func_name = msg_d[event]
                        if func_name in self.event_queue:
                            self.event_queue[func_name].append(event)
                except:
                    print 'event register error'
                    continue

    def zmq_message_parser(self, msg):
        msg = msg.lstrip(ZMQ_PREFIX)
        try:
            res = json.loads(msg)
        except:
            res = None
        return res

    def zmq_json_msg(self, d):
        if isinstance(d, dict):
            res = json.dumps(d)
        return res or ''

    # can override here for different work!!!
    def update_event_status(self):

        new_event_status = {}
        for event in self.event_monitors:
            self.event_monitors[event](self.event_queue[event],
                                       self.reg_event_status)

        # for reg_event in self.reg_event_set:
        #
        #     self.event_monitors[reg_event](self.reg_event_set[])

        # EventMonitors.update_file_mtime(self.reg_event_set, self.reg_event_status)

        # if event status not change
        if self.reg_event_status_last == self.reg_event_status:
            return new_event_status

        for key in self.reg_event_status:
            if not self.reg_event_status == self.reg_event_status_last:
                new_event_status[key] = self.reg_event_status[key]

        self.reg_event_status_last = copy.deepcopy(self.reg_event_status)
        print new_event_status

        return new_event_status


    def run(self):
        ZMQ_JSON_MSG = lambda x : ZMQ_MSG(self.zmq_json_msg(x))
        th = threading.Thread(target=self.event_register)
        th.setDaemon(True)
        th.start()
        with zmq_pub_socket() as pub_socket:
            while 1:
                # update event status
                new_status =  self.update_event_status()
                if new_status:
                    # use zmq_pub to publish msg
                    msg = ZMQ_JSON_MSG(new_status)
                    pub_socket.send(msg)

                time.sleep(1)


if __name__ == '__main__':
    # zmq_server()

    try:
        ser = ZmqPubServer()
        # ser.event_register()
        ser.run()
    except KeyboardInterrupt:
        from zmq_sub import zmq_req_socket
        with zmq_req_socket() as req_socket:
            req_socket.send(ZMQ_EXIT)
            req_socket.recv()
        print 'ZmqPubServer: Quit...'
    pass


