#!/usr/bin/env python
# coding=utf-8

import sys
import traceback
def get_cur_info():
    print sys._getframe().f_code.co_name
    print sys._getframe().f_back.f_lineno
    traceback.print_exc()
    # print sys._getframe().f_back.f_code.co_name

get_cur_info()
