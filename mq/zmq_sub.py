#!/usr/bin/env python
# coding=utf-8

import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5000")
socket.setsockopt(zmq.SUBSCRIBE, "zmq")


while 1:
    print socket.recv()
