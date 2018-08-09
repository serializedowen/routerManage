#!/usr/bin/env python
# coding: utf-8
# coding: cp950

'''
Create Date: 2012-11-06
Version: 1.0
Description: Detection host survival
Author: Victor
QQ: 1409175531
'''

''' Please run the script with root '''

import ping
import sys


def help():
    print(sys.argv[0])
# Usage:
# %s <Dest_addr> <percent loss packages> <max round trip time>
#  % ()


try:
    result = ping.quiet_ping(sys.argv[1], timeout=2, count=10, psize=64)
    if int(result[0]) == 100:
        print(result[0])
        print(int(sys.argv[2]))
        print(int(sys.argv[3]))
        # 'Critical - 宕机, 丢包率:%s%% | 报警阀值: >= %s%% 或 >=%s ms' % (, , )
        sys.exit(2)
    else:
        max_time = round(result[1], 2)
        if int(result[0]) < int(sys.argv[2]) and int(result[1]) < int(sys.argv[3]):
            print(result[0])
            print(max_time)
            print(int(sys.argv[2]))
            print(int(sys.argv[3]))
            # 'OK - 丢包率:%s%%, 最大响应时间:%s ms | 报警阀值: >= %s%% 或 >=%s ms' % (
            # , , , )
            sys.exit(0)
        elif int(result[0]) >= int(sys.argv[2]) or int(result[1]) >= int(sys.argv[3]):
            print(result[0])
            print(max_time)
            print(int(sys.argv[2]))
            print(int(sys.argv[3]))
            # 'Warning - 丢包率:%s%%, 最大响应时间:%s ms | 报警阀值: >= %s%% 或 >=%s ms' % (
            # , , , )
            sys.exit(1)
        else:
            print('Unknown')

            sys.exit(3)
except IndexError:
    help()
    sys.exit(3)
