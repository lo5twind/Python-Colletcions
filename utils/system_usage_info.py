#!/usr/bin/env python
# coding=utf-8

from __future__ import division
import os
import psutil
import json

# INFO_PATH = r'/usr/local/bluedon/log/sys_info.json'
INFO_PATH = r'/tmp/sys_info.json'

def get_disk_total_info():
    p_total = 0
    p_used = 0
    for part in psutil.disk_partitions():
        p = part.mountpoint

        p_info = psutil.disk_usage(p)
        p_total += p_info.total
        p_used += p_info.used

    return p_used/1024/1024, p_total/1024/1024

def get_system_usage_info():

    info = {'cpu':0,
            'mem_total': 0, 'mem_used': 0,
            'root_total': 0, 'root_used': 0,
            'var_total': 0, 'var_used': 0
            }

    info['cpu'] = psutil.cpu_percent(interval=1)

    info['mem_total'] = psutil.virtual_memory().total/1024
    info['mem_used'] = psutil.virtual_memory().used/1024

    root_info = psutil.disk_usage('/')
    info['root_total'] = root_info.total/1024/1024
    info['root_used'] = root_info.used/1024/1024

    var_info = psutil.disk_usage('/var')
    info['var_total'] = var_info.total/1024/1024
    info['var_used'] = var_info.used/1024/1024

    for key in info:
        if key == 'cpu':
            pass
        else:
            info[key] = int(round(info[key]))




    os.system('')
    js = json.dumps(info)
    with open(INFO_PATH, 'w') as fp:
        fp.write(js)

    return js



if __name__ == '__main__':
    get_system_usage_info()
    pass
