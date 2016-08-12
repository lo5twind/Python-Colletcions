#!/usr/bin/env python
# coding=utf-8

import pyotp


if __name__ == '__main__':
    import sys
    sk = 'G6AUXTGVYUUQAEQW4Y2TVWW2KM'
    totp = pyotp.TOTP(sk)
    print totp.verify(sys.argv[1])
    google = 'https://chart.googleapis.com/chart?chs=200x200&chld=M|0&cht=qr&chl='
    qr_url = google + totp.provisioning_uri('lo5twind@gmail.com')
    print qr_url
    print totp.provisioning_uri('lo5twind@gmail.com')


