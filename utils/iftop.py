#!/usr/bin/env python
# coding=utf-8


"""
    2016-10-10:
        Plus all tx/rx as global interface rate
    2016-10-18:
        Use interface with smaller number as inter-net
    2016-10-26:
        Use just one interface's data of a 2-interface bridge
    2016-11-04:
        Get PortMode from Database
"""

from __future__ import division
import os
import psutil
import time
import operator

SAMPLE_PERIOD = 2 # seconds
_rx = operator.itemgetter(0)
_tx = operator.itemgetter(1)

_pre_pre_ns = {}
_MAX_TRAFFIC = {'ERROR_TYPE': 1000,'1000M': 1000, '10000M': 10000}

def bytes2human(n):
    """
        >>> bytes2human(10000)
        '9.8 K'
        >>> bytes2human(100001221)
        '95.4 M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return '%.2f B' % (n)


def bits2human(n):
    """
        >>> bytes2human(10000)
        '9.8 K'
        >>> bytes2human(100001221)
        '95.4 M'
    """
    symbols = ('Kb', 'Mb', 'Gb', 'Tb', 'Pb', 'Eb', 'Zb', 'Yb')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return '%.2f b' % (n)


def is_vEth(x):
    return x[0:4] == 'vEth'


def get_net_io():
    _net_io = {}
    stat = psutil.net_io_counters(pernic=True)
    for ifname in stat:
        if is_vEth(ifname):
            _net_io[ifname] = (stat[ifname].bytes_recv,
                               stat[ifname].bytes_sent)
    return _net_io


def print_net_speed(ns):
    os.system('clear')
    print('{:<6}:  {:<16}| {:<16}'.format('IFace','IN','OUT'))
    for vEth in sorted(ns):
        print('{:<6}:  {:<16}| {:<16}'.format(vEth,ns[vEth]['IN'], ns[vEth]['OUT']))


def add_unit(i):
    i = int(i)/1048576
    return round(i, 4) if i < 1 else round(i, 2)


def get_net_speed(_pre_io, pre_sp_t, nat=None, bridges=None, portsinfo=None, pre_sp={}, iftype={}):
    """
        @param _pre_io[dict]: Rx/Tx Bytes of every interface last time
        @param pre_sp_t[dict]: last speed update time of every interface
        @param portsinfo[dict]: interface type, 1: 2:
    """
    ns = {}
    _ns = {}
    raw_ns = {}
    post_ns = {}   # save net speed after process
    gin, gout = (0, 0)
    _cur_io = get_net_io()
    _cur_t = time.time()
    cur_sp_t = {}
    # print _cur_io
    # print _pre_io
    # print dt

    for vEth in _cur_io:
        # try:
        if vEth not in _pre_io:
            _pre_io[vEth] = (0, 0)

        if vEth not in pre_sp_t:
            pre_sp_t[vEth] = tuple([time.time()] * 2)

        if vEth not in pre_sp:
            pre_sp[vEth] = (0, 0)

        max_sp = _MAX_TRAFFIC.get(iftype.get(vEth, 0), 1000) * 1048576 / 8

        """
            IN  ---> download
            OUT ---> upload
        """

        # process rx
        cur_rx_io = _rx(_cur_io[vEth])
        pre_rx_io = _rx(_pre_io[vEth])
        pre_rx_t = _rx(pre_sp_t[vEth])
        cur_rx_t = pre_rx_t
        pre_rx_sp = _rx(pre_sp[vEth])
        if abs(_cur_t - pre_rx_t) > SAMPLE_PERIOD: # sample time period
            if cur_rx_io == pre_rx_io: # IO bytes not change yet
                # IO does not change in sample period, speed is 0
                cur_rx_sp = 0
            else:
                # IO bytes change
                cur_rx_sp = (cur_rx_io - pre_rx_io) / abs(_cur_t - pre_rx_t)
            # update time
            cur_rx_t = _cur_t
        else: # during sample period, keep speed
            cur_rx_sp = pre_rx_sp
            
        # result filter
        if abs(cur_rx_sp - pre_rx_sp) > 0.25 * pre_rx_sp and pre_rx_sp > 0:
            # cur_rx_sp = 0.25 * (cur_rx_sp - pre_rx_sp) + pre_rx_sp
            if cur_rx_sp > 0.25 * max_sp or cur_rx_sp < pre_rx_sp:
                cur_rx_sp = 1.25 * pre_rx_sp if cur_rx_sp > pre_rx_sp else 0.75 * pre_rx_sp

        cur_rx_sp = min(cur_rx_sp, max_sp)
            
        # process tx
        cur_tx_io = _tx(_cur_io[vEth])
        pre_tx_io = _tx(_pre_io[vEth])
        pre_tx_t = _tx(pre_sp_t[vEth])
        cur_tx_t = pre_tx_t
        pre_tx_sp = _tx(pre_sp[vEth])
        if abs(_cur_t - pre_tx_t) > SAMPLE_PERIOD: # sample time period
            if cur_tx_io == pre_tx_io: # IO bytes not change yet
                # IO does not change in sample period, speed is 0
                cur_tx_sp = 0
            else:
                # IO bytes change
                cur_tx_sp = (cur_tx_io - pre_tx_io) / abs(_cur_t - pre_tx_t)
            # update time
            cur_tx_t = _cur_t
        else: # during sample period, keep speed
            cur_tx_sp = pre_tx_sp
            
        # result filter
        if abs(cur_tx_sp - pre_tx_sp) > 0.25 * pre_tx_sp and pre_tx_sp > 0:
            # cur_tx_sp = 0.25 * (cur_tx_sp - pre_tx_sp) + pre_tx_sp
            if cur_tx_sp > 0.25 * max_sp or cur_tx_sp < pre_tx_sp:
                cur_tx_sp = 1.25 * pre_tx_sp if cur_tx_sp > pre_tx_sp else 0.75 * pre_tx_sp

        cur_tx_sp = min(cur_tx_sp, max_sp)

        # update speed time
        pre_sp_t[vEth] = (cur_rx_t, cur_tx_t)
        # update pre_sp
        pre_sp[vEth] = (cur_rx_sp, cur_tx_sp)
            
        # if nat is not None and vEth in nat:
        if portsinfo is not None and vEth in portsinfo:
            if str(portsinfo.get(vEth, 0)) == '1':
                ns[vEth] = {'IN': bits2human(cur_rx_sp * 8),
                            'OUT': bits2human(cur_tx_sp * 8)}

                _ns[vEth] = {'IN': add_unit(cur_tx_sp * 8),
                             'OUT': add_unit(cur_rx_sp * 8)}

                gin += cur_tx_sp * 8
                gout += cur_rx_sp * 8

            # else:
            # outer-port
            elif str(portsinfo.get(vEth, 0)) == '2':
                ns[vEth] = {'IN': bits2human(cur_tx_sp * 8),
                            'OUT': bits2human(cur_rx_sp * 8)}

                _ns[vEth] = {'IN': add_unit(cur_rx_sp * 8),
                             'OUT': add_unit(cur_tx_sp * 8)}

        else:
            _ns[vEth] = {'IN': add_unit(cur_rx_sp * 8),
                         'OUT': add_unit(cur_tx_sp * 8)}
            ns[vEth] = {'IN': bits2human(cur_rx_sp * 8),
                        'OUT': bits2human(cur_tx_sp * 8)}


    _ns['GLOBAL'] = {'IN': add_unit(gin), 'OUT': add_unit(gout)}
    ns['GLOBAL'] = {'IN': bits2human(gin), 'OUT': bits2human(gout)}

    # print _ns
    # print ns
    return _cur_io, pre_sp_t, ns, _ns


class NetIO(object):
    def __init__(self):
        pass

if __name__ == '__main__':
    pre_io = get_net_io()
    # pre_t = time.time()
    pre_t = {}
    speed = {}
    try:
        while 1:
            pre_io, pre_t, speed, _  = get_net_speed(pre_io, pre_t)
            print_net_speed(speed)

            time.sleep(2)
    except KeyboardInterrupt:
        pass
    pass
