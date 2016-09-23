#!/usr/bin/env python
# coding=utf-8

import sys
import zmq
import time
import json
import threading
from contextlib import contextmanager
from zmq_conf import *

__all__ = ['zmq_sub_socket', 'zmq_req_socket']


def zmq_sub():
    try:
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://127.0.0.1:5000")
        socket.setsockopt(zmq.SUBSCRIBE, "zmq")
        while 1:
            print socket.recv()
    except KeyboardInterrupt as e:
        print 'zmq_sub quit...'
        socket.close()
        sys.exit(e)

def zmq_client(ci):
    try:
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://127.0.0.1:5001")
        count = 1
        while 1:
            msg = '%s : count[%s]' % (ci, count)
            socket.send('%s : count[%s]' % (ci, count))
            req_status =  socket.recv()
            print msg + ' send result[%s]' % (req_status == msg)
            count += 1
            time.sleep (1)
    except KeyboardInterrupt as e:
        print 'zmq_sub client...'
        socket.close()
        sys.exit(e)


@contextmanager
def zmq_sub_socket():
    try:
        sub_context = zmq.Context()
        sub_socket = sub_context.socket(zmq.SUB)
        sub_socket.connect(ZMQ_ADDR.format(port=SUB_POTR))
        sub_socket.setsockopt(zmq.SUBSCRIBE, ZMQ_PREFIX)
        yield sub_socket
    finally:
        print 'ZmqSubClient: sub_socket Exit'
        sub_socket.close()


@contextmanager
def zmq_req_socket():
    try:
        req_context = zmq.Context()
        req_socket = req_context.socket(zmq.REQ)
        req_socket.connect(ZMQ_ADDR.format(port=REQ_POTR))
        yield req_socket
    finally:
        print 'ZmqSubClient: req_socket Exit'
        req_socket.close()


class ZmqSubClient(threading.Thread):
    def __init__(self):
        super(ZmqSubClient, self).__init__()

        self.reg_event = {}
        self.exit = threading.Event()


    def add_event_handler(self, event, handler):
        if not self.reg_event.has_key(event):
            self.reg_event[event] = []

        self.reg_event[event].append(handler)

    def event_change_handler(self, event):
        if not isinstance(self.reg_event[event], list):
            raise TypeError('ZmqSubClient: TypeError %s is not a list' % event)

        for h in self.reg_event[event]:
            if callable(h):
                h()


    def zmq_message_parser(self, msg):
        msg = msg.lstrip(ZMQ_PREFIX)
        try:
            res = json.loads(msg)
        except:
            res = None
        return res

    def register_event(self, event, event_type=None, handler=None):
        event_msg = json.dumps({event : event_type})
        with zmq_req_socket() as req_socket:
            req_socket.send(event_msg)
            msg = req_socket.recv()
            if msg == event_msg:
                self.add_event_handler(event, handler)
                print 'ZmqSubClient: add event[%s] Success...' % event
            else:
                print 'ZmqSubClient: add event[%s] Error...' % event


    def process_message(self, dmsg):
        if not dmsg:
            return None
        print dmsg
        pass

    def run(self):
        with zmq_sub_socket() as sub_socket:
            while 1:
                if self.exit.isSet():
                    break
                msg = sub_socket.recv()
                print 'ZmqSubClient: get msg[%s]' % msg
                self.process_message(self.zmq_message_parser(msg))

            pass
        print 'exit zmq_sub_socket'

    def exit_sub(self):
        print 'exit'
        self.exit.set()
        with zmq_req_socket() as req_socket:
            req_socket.send(ZMQ_SUB_EXIT)
            msg = req_socket.recv()
        print 'exit'
        pass

if __name__ == '__main__':
    import sys
    # zmq_client(sys.argv[1])
    # collecting to server, if server is down, exit
    # init class Eventmonitors
    from zmq_pub import EventMonitors
    EventMonitors()
    cli = ZmqSubClient()
    try:
        cli.register_event(sys.argv[1], event_type=EventMonitors.UPDATE_FILE_MTIME)
        cli.register_event(sys.argv[2], event_type=EventMonitors.UPDATE_FILE_MTIME)
        # cli.run()
        cli.setDaemon(True)
        cli.start()
        time.sleep(2)
    except KeyboardInterrupt:
        print 'ZmqSubClient: Quit...'
    finally:
        cli.exit_sub()
