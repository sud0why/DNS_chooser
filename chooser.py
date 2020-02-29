# -*- coding: utf-8 -*-
import sys
import time
import os
import re
import prettytable as pt
from libping import do_one
from libtcping import tcp_do_one
from udp_test import udp_do_one

server_list = ["114.114.114.114", "114.114.115.115","1.2.4.8", "210.2.4.8", "119.29.29.29", "223.5.5.5", "223.6.6.6", "180.76.76.76", "101.226.4.6", "218.30.118.6", "123.125.81.6", "140.207.198.6"]
port = 53
type = "udp"
header = ['ip', 'rtt']


def mainloop(data):
    p = pt.PrettyTable()
    p.field_names = header

    for key in data.keys():
        row_data = [key, data[key]]
        p.add_row(row_data)

    os.system('clear')
    sys.stdout.write("{0}".format(p))
    sys.stdout.flush()
    sys.stdout.write("\n")
    time.sleep(10)


# header = ['type', 'ip', 'count', 'avg', 'min', 'max', 'loss']

all_data = {}


while True:
    # for index, server in enumerate(server_list):
    for server in server_list:
        if type == "tcp":
            rtt = tcp_do_one(server, 53)
        elif type == "udp":
            rtt = udp_do_one(server, 53)
        else:
            rtt = do_one(server, 1, 32)

        if rtt:
            all_data[server] = rtt
        else:
            all_data[server] = float("inf")
    mainloop(all_data)
