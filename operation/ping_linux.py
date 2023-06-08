# -- coding:UTF-8 --
# !/usr/bin/env python
"""

"""

from os import system
from utils import GetResourceFromMongo


class PingLinux:
    def __init__(self):
        obj = GetResourceFromMongo()
        self.worker_ips = obj.get_ip()
        self.res = []

    # 定义ping函数
    def ping_pc(self, ipaddr):
        end = system("ping -c2 -i0.2 -w2 %s  &> /dev/null" % (ipaddr))  # 每次发生2个包，间隔0.2秒，最长等待2秒将信息不显示输出
        if end == 0:  # 表示ping通
            return ("%s up" % ipaddr)
        else:  # 表示不通
            return ("%s down" % ipaddr)

    def main(self):
        for ip in self.worker_ips:
            self.res.append(f'{self.ping_pc(ip)}')
        return self.res


if __name__ == "__main__":
    print(PingLinux()())
