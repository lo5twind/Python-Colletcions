#!/usr/bin/env python
# coding=utf-8

from mysql import execute_sql


if __name__ == '__main__':
    sql = 'select *1 from m_tbnetport;'
    try:
        execute_sql(sql)
    except:
        print 'error'
