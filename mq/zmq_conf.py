#!/usr/bin/env python
# coding=utf-8


# subscriber port
SUB_POTR = 5000
# request port
REQ_POTR = 5001
# publisher port
PUB_POTR = 5000
# response port
REP_POTR = 5001

ZMQ_ADDR = "tcp://127.0.0.1:{port:}"
ZMQ_PREFIX = r'ZMQ://'
ZMQ_MSG = lambda x : ZMQ_PREFIX + x
ZMQ_STAT = lambda ty, msg : ZMQ_MSG("{%s:'%s'}" % (ty, msg))

# common MSG
ZMQ_INVALIDE_MSG = ZMQ_STAT('error', 'invalide message')


# publisher MSG
ZMQ_EXIT = ZMQ_STAT('command', 'exit')


# subscriber MSG
ZMQ_SUB_EXIT = ZMQ_STAT('exit_sub', 'command')
