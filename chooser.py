# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import json
from pythonping import ping
import prettytable as pt


class Chooser:
    def __init__(self, config_file="config.json"):
        with open(config_file, 'r') as load_f:
            self.config = json.load(load_f)
        self.server_cn = self.config["server_cn"]
        self.server_global = self.config["server_global"]
        self.method = self.config["method"]
        self.timeout = self.config["timeout"]
        self.count = self.config["count"]
        self.result = {}
        for ip in self.server_cn:
            self.result[ip] = {}
        print(self.config)

    def icmp_once(self, ip):
        time_start = time.time()
        while True:
            result = ping(ip, timeout=self.timeout, count=self.count, payload="A" * 32, match=True)
            if result.success(2) and abs(result.rtt_avg_ms - result.rtt_min_ms) < 5:
                return result.rtt_avg_ms
            if time.time() - time_start > 30:
                if result.rtt_avg_ms < 1000:
                    return result.rtt_avg_ms
                else:
                    return float("inf")

    def check_icmp(self):
        for ip in self.server_cn:
            self.result[ip]["icmp"] = self.icmp_once(ip)

    def print_result(self):
        result_output = sorted(self.result.items(), key=lambda info: info[1]["icmp"])
        result_table = pt.PrettyTable()
        result_table.field_names = ["ip", "icmp"]
        for each_item in result_output:
            result_table.add_row([each_item[0], each_item[1]['icmp']])
        print(result_table)


if __name__ == "__main__":
    chooser = Chooser()
    chooser.check_icmp()
    chooser.print_result()
