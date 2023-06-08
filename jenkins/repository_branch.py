import paramiko
from utils import GetResourceFromMongo


class BranchName:
    def __init__(self, command=None, hostname=None, file=None):
        self.file = file if file else '/root.pem'
        self.command = command if command else 'python get_jenkins_repository_version.py'
        self.hostname = hostname if hostname else '172.30.6.82'

        obj = GetResourceFromMongo()
        self.dict = obj.get_jenkins()

    def sftp_client_con(self):
        hostname = self.hostname
        username = self.dict[self.hostname]['username']
        password = self.dict[self.hostname]['password']
        port = self.dict[self.hostname]['port']
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port, username, password, compress=True)
        sftp_client = client.open_sftp()
        remote_file = sftp_client.open(self.file)  # 文件路径
        try:
            for line in remote_file:
                print(line)
        finally:
            remote_file.close()

    def ssh_client_con(self):
        """创建ssh连接，并执行shell指令"""
        # 1 创建ssh_client实例
        ssh_client = paramiko.SSHClient()
        # 自动处理第一次连接的yes或者no的问题
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        # 2 连接服务器
        ssh_client.connect(
            hostname=self.hostname,
            username=self.dict[self.hostname]['username'],
            password=self.dict[self.hostname]['password'],
            port=self.dict[self.hostname]['port'],
        )

        # 3 执行shell命令
        # 构造shell指令
        shell_command = self.command
        # 执行shell指令
        stdin, stdout, stderr = ssh_client.exec_command(shell_command)
        # 输出返回信息
        stdout_info = stdout.read().decode('utf8').strip("\n")
        return stdout_info

        # 输出返回的错误信息
        # stderr_info = stderr.read().decode('utf8')
        # print(stderr_info)


if __name__ == '__main__':
    demo = BranchName(command='df -h', hostname='172.30.6.82')
    demo.ssh_client_con()
    # # demo.ssh_client_con(command='df -h', hostname='172.30.6.82')
    # demo.sftp_client_con(file='/root.pem', hostname='172.30.6.82')
