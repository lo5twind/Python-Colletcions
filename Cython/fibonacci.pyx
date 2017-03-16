#!/usr/bin/env python
# coding=utf-8

def fib(n):
    cdef int a, b
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


