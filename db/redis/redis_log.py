#!/usr/bin/env python
# coding=utf-8

import sys
import redis
import time
from redis_config import *
from redis_op import create_redis
from contextlib import contextmanager

_RS = create_redis()

class LogTime(object):
    def __init__(self, _ts):
        super(LogTime, self).__init__()
        self.timestamp = _ts
        self.timetuple = time.localtime(float(_ts))
        self.date = time.strftime("%Y%m%d", self.timetuple)

def redis_write_log(_rs, _logtype, _logtime, _logline):
    log_time = LogTime(_logtime)
    table_name = _logtype + '_' + log_time.date
    log_key = _logtype + '_' + log_time.timestamp

    # push log_key in a list(table_name)
    if not _rs.exists(log_key):
        _rs.lpush(table_name, log_key)

    # put log line in a list(log_key)
    _rs.lpush(log_key, _logline)


    pass
def redis_read_log(_rs, _logtype, _logtime):
    log_time = LogTime(_logtime)
    table_name = _logtype + '_' + log_time.date
    log_key = _logtype + '_' + str(log_time.timestamp)
    ret = list()

    print log_key

    # for key in _rs.lrange(table_name, 0, -1):
    for _logline in _rs.lrange(log_key, 0, -1):
        ret.append(_logline)

    print ret
    pass


if __name__ == '__main__':
    with open('/root/tmp/iptables-ng.log', 'r') as fp:
        log_lines = fp.readlines()

    for line in log_lines:
        log_time = line.split()[0]
        redis_write_log(_RS, 'firewall', log_time, line)

    print log_lines[-1]
    redis_read_log(_RS, 'firewall', 1479811982)
    pass

