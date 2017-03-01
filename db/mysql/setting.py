# -*- coding: utf-8 -*-

import MySQLdb, MySQLdb.cursors
import logging


# 全局日志级别
# 可选级别：logging.NOTSET, logging.DEBUG, logging.INFO,
#           logging.WARNING, logging.ERROR, logging.CRITICAL
LOG_LEVEL = logging.NOTSET


# 数据库链接
DB = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': '123',
    'db': 'db1',
    'charset': 'utf8',
    'use_unicode':True,
    # 'unix_socket': '/tmp/mysql3306.sock',
}

DICT_DB = {
    'host': 'localhost',
    'port': 3306,
    'user': 'username',
    'passwd': 'passwd',
    'db': 'dbname',
    'charset': 'utf8',
    'use_unicode':True,
    'cursorclass': MySQLdb.cursors.DictCursor,
    'unix_socket': '/tmp/mysql3306.sock'
}

LOG_DB = {
    'host': 'localhost',
    'port': 3307,
    'user': 'username',
    'passwd': 'passwd',
    'db': 'dbname',
    'charset': 'utf8',
    'use_unicode':True,
    'unix_socket': '/tmp/mysql3306.sock',
}

DICT_LOG_DB = {
    'host': 'localhost',
    'port': 3307,
    'user': 'username',
    'passwd': 'passwd',
    'db': 'dbname',
    'charset': 'utf8',
    'use_unicode':True,
    'cursorclass': MySQLdb.cursors.DictCursor,
    'unix_socket': '/tmp/mysql3306.sock'
}
