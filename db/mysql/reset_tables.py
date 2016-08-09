#!/usr/bin/env python
# coding=utf-8

import os
import sys
from mysql import DB


SQL_FILE = './db_tb.sql'

def TB_SQL(tb, sql_file=SQL_FILE):
    return get_tb_sql(tb, sql_file)


def get_tb_sql(tb, sql_file=SQL_FILE):
    with open(sql_file, 'r') as fp:
        lines = fp.readlines()
    try:
        start_line = 'DROP TABLE IF EXISTS `%s`;\n' % tb
        idx_start = lines.index(start_line) + 1
    except ValueError:
        start_line = 'DROP TABLE IF EXISTS `%s`;\r\n' % tb
        idx_start = lines.index(start_line) + 1
    lines[idx_start] = 'CREATE TABLE IF NOT EXISTS `%s` (\n' % tb
    idx_end = idx_start
    count = idx_start
    for line in lines[idx_start:]:
        if ';' in line:
            # idx_end = lines.index(line) + 1
            idx_end = count + 1
            break
        count += 1
    return ''.join(lines[idx_start:idx_end]).strip('\n')




def reset_tables():
    tb_sql = SQL_FILE
    if not os.path.exists(tb_sql):
        print 'No sql file [%s]' % tb_sql
        return
    cmd = ("/usr/bin/mysql --port={port:} --socket={sock:} "
           "-u{usr:} --password={pwd} -e 'source %s'").format(port=DB['port'],
                                                              sock=DB['unix_socket'],
                                                              usr=DB['user'],
                                                              pwd=DB['passwd'])
    os.system(cmd % tb_sql)
    print cmd
    pass

if __name__ == '__main__':
    reset_tables()
    pass
