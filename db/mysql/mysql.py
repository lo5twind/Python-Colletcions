#!/usr/bin/env python
# coding=utf-8

"""
config file
"""

import MySQLdb, MySQLdb.cursors
import os


# fetch result will return a dict
DB = {
        'host': 'localhost',
        'port': 0,
        'user': 'username',
        'passwd': 'passwd',
        'db': 'dbname',
        'charset': 'utf8',
        #'use_unicode':False,
        'cursorclass': MySQLdb.cursors.DictCursor,
        'unix_socket': '/tmp/sockname.sock'
        }

# fetch result will return a list
DB1 = {
        'host': 'localhost',
        'port': 0,
        'user': 'username',
        'passwd': 'passwd',
        'db': 'dbname',
        'charset': 'utf8',
        #'use_unicode':False,
        # 'cursorclass': MySQLdb.cursors.DictCursor,
        'unix_socket': '/tmp/sockname.sock'
        }


def search_data(sql):
    """
    执行sql语句
    args:
        sql: 查询的sql语句
    return:
        datas: 查询的记录集
    """

    conn = MySQLdb.connect(**DB)
    cur = conn.cursor()
    cur.execute(sql)
    datas = cur.fetchall()
    conn.close()
    return datas

def execute_sql(sql):
    """ 执行sql语句 """

    conn = MySQLdb.connect(**DB)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
    #except:
    #    conn.rollback()
    #debug
    except Exception as e:
        print e
        conn.rollback()
    conn.close()





def executemany_sql(sql,args):
    """
        执行sql语句
        args:
            sql: 要重复执行的SQL语句
            args: 一个列表,列表中的元素为SQL语句的参数(Tuple)
    """
    if args == []:
        return
    conn = MySQLdb.connect(**DB)
    cur = conn.cursor()
    try:
        cur.executemany(sql,args)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print e
    conn.close()


def get_mysql_db():
    """ 获取数据库链接和游标  """

    try:
        conn = MySQLdb.connect(**DB)
        cur = conn.cursor()
        return conn,cur
    except:
        return None,None

def get_mysql_db1():
    """ 获取数据库链接和游标  """

    try:
        conn = MySQLdb.connect(**DB1)
        cur = conn.cursor()
        return conn,cur
    except:
        return None,None

def fetchone_sql(sql):
    """
    执行sql语句
    args:
        sql: 查询的sql语句
    return:
        datas: 查询的记录集
    """

    conn = MySQLdb.connect(**DB)
    cur = conn.cursor()
    cur.execute(sql)
    datas = cur.fetchone()
    cur.close()
    conn.close()
    return datas


def fetchall_sql(sql):
    """
    执行sql语句
    args:
        sql: 查询的sql语句
    return:
        datas: 查询的记录集Iterable对象
    """

    conn = MySQLdb.connect(**DB)
    cur = conn.cursor()
    cur.execute(sql)
    datas = cur.fetchall()
    cur.close()
    conn.close()
    for res in datas:
        yield res

def record_in_tb(val,attr,tb):
    """
    检查tb数据表中是否存在值为val的字段attr
    args:
        val:字段值
        attr:字段名
        tb:数据表名
    """
    sql = 'select %s from %s where %s="%s" limit 1'
    res = fetchone_sql(sql % (attr,tb,attr,val))
    return res != None
