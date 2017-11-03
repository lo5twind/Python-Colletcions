#!/usr/bin/env python
# coding=utf-8

import re
import sys
import json
from collections import OrderedDict

reload(sys)
sys.setdefaultencoding('utf-8')

def sql_to_csv():
    with open('/usr/local/bluedon/tmp/Mysql_3307_product_20160908.sql') as fp:
        lines = fp.readlines()

    table_name = None
    ret = OrderedDict()
    all_ret = OrderedDict()
    all_ret_cmt = OrderedDict()
    for line in lines:
        if 'CREATE TABLE' in line:
            m = re.search('`.*`', line, re.DOTALL)
            if m is not None:
                table_name = m.group()[1:-1]
                print table_name
        elif 'DROP TABLE IF EXISTS' in line:
            pass
        elif 'ENGINE=' in line:
            # last of a sql
            print ret
            m = re.search('COMMENT=\'.*\'', line, re.DOTALL)
            if m is not None:
                tb_cmt = m.group().replace('COMMENT=', '')[1:-1]
                all_ret_cmt[table_name] = tb_cmt
            else:
                all_ret_cmt[table_name] = '无'
            all_ret[table_name] = ret
            ret = OrderedDict()
            table_name = None
        else:
            if table_name and 'KEY' not in line:
                # find field name
                m = re.search('`.*`', line, re.DOTALL)
                if m is not None:
                    key = m.group()

                # find field comment
                m = re.search('COMMENT \'.*\'', line, re.DOTALL)
                if m is not None:
                    ftype = line.replace(key, '').replace(m.group(), '').replace(',', '').strip()
                    val = m.group().replace('COMMENT ', '')
                else:
                    ftype = line.replace(key, '').replace(',', '').strip()
                    val = '-'

                key = key[1:-1]
                val = val[1:-1].replace("'", '')


                ret[key] = [ftype, val]


    with open('/usr/local/bluedon/tmp/sql_to_csv_result.csv', 'w') as fp:
        for table_name in all_ret:
            fp.write('"表名"\t"%s"\t"%s"\n' % (table_name, all_ret_cmt[table_name]))
            fp.write('"字段名"\t"字段类型"\t"字段说明"\n')
            tb_fields = all_ret[table_name]
            for field_name in tb_fields:
                fields = tb_fields[field_name]
                fp.write('"%s"\t "%s"\t"%s"\n' % (field_name, fields[0], fields[1]))


    # with open('/usr/local/bluedon/tmp/sql_to_csv_result', 'w') as fp:
    #     json.dump(all_ret, fp, ensure_ascii=False)


if __name__ == '__main__':
    sql_to_csv()
    pass
