#!/usr/bin/env python
# coding=utf-8

import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5000")
count = 0
while 1:
    socket.send("zmq send [%s]" % count)
    count += 1
    time.sleep(1)


