# -- coding:UTF-8 --
# !/usr/bin/env python
"""

"""
import paramiko
from utils import GetResourceFromMongo


class ServicePath:
    def __init__(self, hostname):
        self.hostname = hostname
        obj = GetResourceFromMongo()
        self.worker_ips = obj.get_password()
        self.service_port = {'lts': '8720', 'jobtracker': '8721', 'yarn_tasktracker': '17030', 'comparison': '8731',
                             'tldw': '8080', 'graph': '8999', 'analyzer': '8051', 'case_management': '8060',
                             'chart_management': '8810', 'data_gov': '18080', 'gateway': '8070', 'dictionary': '8820', }

    def get_cmd_result(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, port=22, username='root', password=self.worker_ips[self.hostname])

        results = []

        for k, v in self.service_port.items():
            cmd = f'''ss -ntpl|grep {v}|awk -F "pid=" {{'print $2'}}|awk -F "," {{'print $1'}}|xargs pwdx'''
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.read().decode('UTF-8')

            if not result:
                result = f"can't find {k} port {v}\n"
            results.append(result)

        return results


if __name__ == '__main__':
    obj = ServicePath('172.30.6.82')
    print(obj.get_cmd_result())
