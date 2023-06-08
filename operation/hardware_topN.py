# -- coding:UTF-8 --
# !/usr/bin/env python
"""

"""
import paramiko
from utils import GetResourceFromMongo


class TopN:
    def __init__(self,hostname, hareware):
        self.hostname = hostname
        self.hardware = hareware
        obj = GetResourceFromMongo()
        self.worker_ips = obj.get_password()


    def get_cmd_result(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, port=22, username='root', password=self.worker_ips[self.hostname])

        cmd = 'whoami'
        if self.hardware == 'CPU':
            cmd = 'ps aux|head -n1;ps aux|grep -v PID|sort -nr -k3|head -n10'
        elif self.hardware == 'MEM':
            cmd = 'ps aux|head -n1;ps aux|grep -v PID|sort -nr -k4|head -n10'

        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read().decode('UTF-8')

        return result


if __name__ == '__main__':
    obj = TopN('172.30.6.82','MEM')
    print(obj.get_cmd_result())

