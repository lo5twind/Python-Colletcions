#!/usr/bin/env python
# coding=utf-8



import time
import datetime
from mysql_observer import MysqlObserver, MysqlOb
from mysql import fetchone_sql as fetch_sql


def handler(*args, **kwargs):
    print args

class Class1(MysqlObserver):
    def __init__(self, key='default1'):
        super(Class1, self).__init__()
        self.ob = MysqlOb(handler)
        self.key = key
        print 'add_observer id='
        print id(self.__class__.add_observer)
        print id(self.__class__.__mro__[1].add_observer)
        self.__class__.__mro__[1].add_observer(self.key, self.ob)
        pass

class Class2(MysqlObserver):
    def __init__(self, key='default2'):
        super(Class2, self).__init__()
        self.ob = MysqlOb(handler)
        self.key = key
        print 'add_observer id='
        print id(self.__class__.add_observer)
        print id(self.__class__.__mro__[1].add_observer)
        self.__class__.__mro__[1].add_observer(self.key, self.ob)
        pass


def watch_mysql():
    now = datetime.datetime.now()
    tb_list = {'m_tblog_ddos':now,
               'm_tblog_ips':now}

    # c1 = Class1(tb_list.keys()[0])
    # c2 = Class2(tb_list.keys()[1])

    for key in tb_list:
        MysqlObserver.add_observer(key, handler)

    query_sql = ('SELECT UPDATE_TIME FROM information_schema.`TABLES` '
                 'WHERE TABLE_NAME="%s";')
    while 1:
        print MysqlObserver.ob_count
        for tb in MysqlObserver.ob:
            res = fetch_sql(query_sql % tb)
            if isinstance(res['UPDATE_TIME'], datetime.datetime):
                if res['UPDATE_TIME'] > tb_list[tb]:
                    tb_list[tb] = res['UPDATE_TIME']
                    MysqlObserver.notify_observer(tb, '%s update at %s' % (tb, res['UPDATE_TIME']))



        pass
        time.sleep(1)


if __name__ == '__main__':
    watch_mysql()
    # observer = MysqlObserver()
    # for i in range(4):
    #     ob = MysqlOb()
    #     observer.add_observer(i, ob)

    # for ob in MysqlObserver.ob:
    #     MysqlObserver.notify_observer(ob, 'notify ob[%s]...' % ob)
    # pass
