#!/usr/bin/env python
# coding=utf-8

import os


def mkdir_file(file_path, cmd_type='file'):
    """
    判断文件路径和文件是否存在, 不存在则创建
    args:
        file_path: 文件路径
        cmd_type: 创建的文件类型
    return:
        None
    """

    cmd_dict = {'file': '/usr/bin/touch',
                'fifo': '/usr/bin/mkfifo'}

    if not os.path.exists(file_path):
        file_split = os.path.split(file_path)
    if not os.path.exists(file_split[0]):
        os.system('mkdir %s' %(file_split[0]))
        os.system('%s %s' %(cmd_dict[cmd_type], file_path))
        os.system('/usr/bin/chmod 777 %s' %(file_path))
        return True
    else:
        return False
