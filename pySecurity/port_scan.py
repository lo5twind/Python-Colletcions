#!/usr/bin/env python
# coding=utf-8

import os
import sys
import socket
import logging
from netaddr import *

# text color
_colorred = "\033[01;31m{0}\033[00m{1}"
_colorgrn = "\033[02;32m{0}\033[00m{1}"

_E = lambda x,y='' : _colorred.format(x, y)
_T = lambda x,y='' : _colorgrn.format(x, y)

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        logging.error('Usage python port_scan.py x.x.x.x/y n-m|n')
        sys.exit()

    # network
    ip_net = IPNetwork(sys.argv[1])
    # port
    start_port = int(sys.argv[2].split('-')[0])
    end_port = int(sys.argv[2].split('-')[-1])

    logging.info('start scanning...{n}'.format(n=str(ip_net)))
    for ip in ip_net:
        ip = str(ip)
        for port in range(start_port, end_port + 1):
            logging.info('start scanning...{ip}:{port}'.format(ip=ip, port=port))
            try:
                s = socket.socket()
                s.settimeout(1)
                s.connect((ip, port))
                s.send('Hello')

                r = s.recv(1024)
            except socket.error:
                logging.error(_E('{ip}:{port} is unreachable'.format(ip=ip, port=port)))
            else:
                logging.info(_T('Find an open port: {ip}:{port}'.format(ip=ip, port=port)))

