#!/usr/bin/env python
# coding=utf-8


import sys
import redis
from redis_op import create_redis
from contextlib import contextmanager


def create_hashset(redis_obj, set_name):
    pass


class RedisHashSet(object):
    def __init__(self, setname):
        super(RedisHashSet, self).__init__()
        self.set_name = setname
        self.key_ = lambda x : 'bdfwlog_redis_hashset_{sn}_{v}'.format(
            sn=self.set_name, v=x)

        self.redis_obj = create_redis(db=2)

    def init_key(self, k):
        self.redis_obj.hset(self.set_name, k, 1)

    def inc_key(self, k):
        self.redis_obj.hincrby(self.set_name, k)

    def del_key(self, k):
        self.redis_obj.hdel(self.set_name, k)

    def get_key(self, k):
        return self.redis_obj.hget(self.set_name, k)

    def get_allkeys(self):
        return self.redis_obj.hgetall(self.set_name)


    def __del__(self):
        self.redis_obj.connection_pool.disconnect()
        pass

if __name__ == '__main__':
    rd = RedisHashSet('test')
    rd.init_key('rd_key1')
    rd.inc_key('rd_key1')
    print rd.get_allkeys()
    pass
