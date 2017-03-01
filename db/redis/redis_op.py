#!/usr/bin/env python
# coding=utf-8

import sys
import redis
from redis_config import *
from contextlib import contextmanager


# subscribe redis channel
@contextmanager
def subscribe_channel(redis_obj, chn):
    try:
        # setup
        ps = redis_obj.pubsub()
        ps.subscribe(chn)
        yield ps.listen()
    except RuntimeError as e:
        print e
    finally:
        # cleanup
        ps.unsubscribe(chn)


def publish_channel(redis_obj, chn, content):
    redis_obj.publish(chn, content)


def create_redis(host=HOST, port=PORT, db=DB):
    try:
        re = redis.Redis(host=host, port=port, db=db)
    except Exception as e:
        re = None
        print e
    return re


if __name__ == '__main__':
    re = create_redis()
    if sys.argv[1] == 'sub':
        try:
            with subscribe_channel(re, SUB_CHANNEL) as sub:
                for i in sub:
                    print i
        except KeyboardInterrupt:
            print 'exit'
    elif sys.argv[1] == 'pub':
        # publish_channel(re, SUB_CHANNEL, 'aaa')
        with open('/root/Desktop/python_test/LogParser/logs/mail.bcp.1473400424', 'r') as fp:
            l = fp.readline()
        CH = 'netlog_email'
        # publish_channel(re, SUB_CHANNEL, 'aaa')
        publish_channel(re, CH, l)
    pass
