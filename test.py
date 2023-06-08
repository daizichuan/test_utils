import paramiko
import re
from dingtalkchatbot.chatbot import DingtalkChatbot

worker_ips = [
    '172.30.6.45',
    '172.30.6.82',
    '172.30.6.123',
    '172.30.6.124',
]


def get_cmd_result(ip, cmd):
    if ip == '172.30.6.82':
        password = 'Jwyc12345!'
    if ip.split('.')[-1] in ['45', '123','124']:
        password = 'zqykj123'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, port=22, username='root', password=password)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read()

    return result


def get_re_result(rule, result):
    result_li = re.findall(rule, result)

    return result_li


def check_cpu():
    cpu_space_ip_dict = {}
    for worker_ip in worker_ips:
        result = get_cmd_result(worker_ip, 'top -bi -n 4 -d 0.02')  # 单独的top命令通过paramiok不会有返回值,-n 表示查看4次,-d 表示隔多久查看一次
        space_li = get_re_result(r', (\d+.\d+) id',
                                 result.decode('UTF-8'))  # 注意：可能由于网络原因，查看4次结果 列表长度不一定就是4，元素个数会<=4，有可能为0
        if space_li:
            # space = 100 - reduce(lambda a,b:float(a) + float(b), space_li) / len(space_li)
            space = 100 - sum([float(x) for x in space_li]) / len(space_li)
            cpu_space_ip_dict[worker_ip] = "%d%%" % space
        else:
            cpu_space_ip_dict[worker_ip] = "【获取服务器数据异常，需手动获取】"

    return cpu_space_ip_dict


def check_df():
    df_space_ip_result = {}
    for worker_ip in worker_ips:
        result = get_cmd_result(worker_ip, 'df /')
        space = get_re_result(r'\d+%', result.decode('UTF-8'))[0]
        df_space_ip_result[worker_ip] = space

    return df_space_ip_result


def check_mem():
    mem_space_ip_dict = {}
    for worker_ip in worker_ips:
        result = get_cmd_result(worker_ip, 'free | grep Mem')
        mem_li = get_re_result(r'\d+', result.decode('UTF-8'))
        mem_space = round(int(mem_li[1]) / int(int(mem_li[0]) + 1e-5), 2) * 100
        mem_space_ip_dict[worker_ip] = f'{mem_space}%'

    return mem_space_ip_dict


def dd_robot(msg):
    secret = "SECe60dbd0f132ac35ac1c6cccba52f46d2ebb7335f8910b65addde7ef19499edc0"
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=97a1026358466729fcb553e997b109af148ed919a74af02de499eb1767c1056f"
    # 机器人初始化
    # :param webhook: 钉钉群自定义机器人webhook地址
    #  :param secret: 机器人安全设置页面勾选“加签”时需要传入的密钥
    #  :param pc_slide: 消息链接打开方式，默认False为浏览器打开，设置为True时为PC端侧边栏打开
    #  :param fail_notice: 消息发送失败提醒，默认为False不提醒，开发者可以根据返回的消息发送结果自行判断和处理

    dd = DingtalkChatbot(webhook=webhook, secret=secret)

    # 发送消息
    # :param msg: 消息内容
    #  :param is_at_all: @所有人时：true，否则为false（可选）
    #  :param at_mobiles: 被@人的手机号（注意：可以在msg内容里自定义@手机号的位置，也支持同时@多个手机号，可选）
    # :param at_dingtalk_ids: 被@人的dingtalkId（可选）
    # :param is_auto_at: 是否自动在msg内容末尾添加@手机号，默认自动添加，可设置为False取消（可选）

    dd.send_text(msg=msg, is_at_all=False, at_mobiles=[])

def analysis():
    cpu_lst = check_cpu()
    disk_lst = check_df()
    mem_lst = check_mem()

    dict_tmp = {}
    for _ in worker_ips:
        dict_tmp[_] = {'cpu': 0, 'disk': 0, 'mem':0 }

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

    for k, v in dict_tmp.items():
        # print(k, v)
        flag = True
        for k1, v1 in v.items():
            value = v1.split('%')[0]
            if int(float(value)) > 70:
                print('+++++++')
                print(k, v)
                print('+++++++')
                dd_robot(f"{k}:{v}")
                flag = False
            if not flag:
                break

if __name__ == '__main__':
    import schedule
    import time
    schedule.every(1).minutes.do(analysis)

    while True:
        schedule.run_pending()
        time.sleep(1)
