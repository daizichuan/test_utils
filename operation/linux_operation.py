import paramiko
import re
from utils import GetResourceFromMongo


class LinuxOperation:
    def __init__(self):
        obj = GetResourceFromMongo()
        self.worker_ips = obj.get_password()

    def get_cmd_result(self, ip, cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, port=22, username='root', password=self.worker_ips[ip])
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()

        return result

    def get_re_result(self, rule, result):
        result_li = re.findall(rule, result)

        return result_li

    def check_cpu(self):
        cpu_space_ip_dict = {}
        for worker_ip in self.worker_ips:
            result = self.get_cmd_result(worker_ip,
                                         'top -bi -n 4 -d 0.02')  # 单独的top命令通过paramiok不会有返回值,-n 表示查看4次,-d 表示隔多久查看一次
            space_li = self.get_re_result(r', (\d+.\d+) id',
                                          result.decode('UTF-8'))  # 注意：可能由于网络原因，查看4次结果 列表长度不一定就是4，元素个数会<=4，有可能为0
            if space_li:
                # space = 100 - reduce(lambda a,b:float(a) + float(b), space_li) / len(space_li)
                space = 100 - sum([float(x) for x in space_li]) / len(space_li)
                cpu_space_ip_dict[worker_ip] = "%d%%" % space
            else:
                cpu_space_ip_dict[worker_ip] = "【获取服务器数据异常，需手动获取】"

        return cpu_space_ip_dict

    def check_df(self):
        df_space_ip_result = {}
        for worker_ip in self.worker_ips:
            result = self.get_cmd_result(worker_ip, 'df /')
            space = self.get_re_result(r'\d+%', result.decode('UTF-8'))[0]
            df_space_ip_result[worker_ip] = space

        return df_space_ip_result

    def check_mem(self):
        mem_space_ip_dict = {}
        for worker_ip in self.worker_ips:
            result = self.get_cmd_result(worker_ip, 'free | grep Mem')
            mem_li = self.get_re_result(r'\d+', result.decode('UTF-8'))
            mem_space = round(int(mem_li[1]) / int(int(mem_li[0]) + 1e-5), 2) * 100
            mem_space_ip_dict[worker_ip] = f'{int(mem_space)}%'

        return mem_space_ip_dict

    def analysis(self):
        cpu_lst = self.check_cpu()
        disk_lst = self.check_df()
        mem_lst = self.check_mem()

        dict_tmp = {}
        for _ in self.worker_ips:
            dict_tmp[_] = {'cpu': 0, 'disk': 0, 'mem': 0}

        lst = []
        lst.append(cpu_lst)
        lst.append(disk_lst)
        lst.append(mem_lst)

        x = 0
        for _ in lst:
            key = ''
            for k, v in _.items():
                if x == 0:
                    key = 'cpu'
                if x == 1:
                    key = 'disk'
                if x == 2:
                    key = 'mem'
                dict_tmp[k][key] = v
            x += 1

        # print(dict_tmp)
        return dict_tmp


if __name__ == '__main__':
    demo = LinuxOperation()

    demo.analysis()
