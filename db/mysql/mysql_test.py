#!/usr/bin/env python
# coding=utf-8

from mysql import execute_sql
from mysql import fetchall_sql as fcal


if __name__ == '__main__':
    sql = 'select * from m_tblog_travelrecord;'
    # execute_sql(sql)
    for r in fcal(sql):
        print r
    # baseid = 10000000
    baseid = 1
    for i in range(1000000):
        k = baseid + i
        # print("INSERT INTO m_tblog_travelrecord (`id`, `sPlace`) VALUES(%s, 'xxx');" % k)
        execute_sql("INSERT INTO m_tblog_travelrecord (`id`, `sPlace`) VALUES(%s, 'xxx');" % k)
    # try:
    #     execute_sql(sql)
    # except:
    #     print 'error'
