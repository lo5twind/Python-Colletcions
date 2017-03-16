#!/usr/bin/env python
# coding=utf-8

import time
from fibonacci import fib

def py_fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
num = 100000
st = time.time()
fib(num)
print 'use time = %f'  % (time.time() - st)

st = time.time()
py_fib(num)
print 'use time = %f'  % (time.time() - st)
