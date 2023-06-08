# -- coding:UTF-8 --
# !/usr/bin/env python
"""

"""
from enum import Enum

import uvicorn
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import os
from faker import Faker
import re
from fastapi.responses import PlainTextResponse
from fastapi.responses import FileResponse

from identity import IdNumber
from social_credit import SocialCredit
from zen_tao import ThisWeekBugsSummary
from zen_tao import VersionBugsSummary
from database import CompareCollections
from database import CompareMysqlDB
from jenkins import BranchName
from operation import LinuxOperation
from zen_tao import CheckBugComment
from zen_tao import Runmain
from operation import PingLinux
from operation import TopN
from operation import ServicePath

from fastapi import applications
from fastapi.openapi.docs import get_swagger_ui_html


def swagger_monkey_patch(*args, **kwargs):
    """
    Wrap the function which is generating the HTML for the /docs endpoint and
    overwrite the default values for the swagger js and css.
    """
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui-bundle.js",
        swagger_css_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui.css")


# Actual monkey patch
applications.get_swagger_ui_html = swagger_monkey_patch

app = FastAPI(
    description="使用方法：点击右上角Try it out。需要输入参数的（required），先输入参数再点击Execute；不需要输入参数的直接点击Execute结果见Response body。\
    直接编辑python脚本，可以使用jupyter notebook：http://172.30.6.82:8003/")


class IP(str, Enum):
    IP45 = "172.30.6.45"
    IP82 = "172.30.6.82"
    IP111 = '172.30.6.111'
    IP123 = "172.30.6.123"
    IP124 = "172.30.6.124"
    IP222 = "172.30.6.222"


class Hardware(str, Enum):
    CPU = "CPU"
    MEM = "MEM"


class Item(BaseModel):
    s_code: str


@app.get("/generate_id", tags=["身份证"], summary="生成身份证", response_class=PlainTextResponse)
async def generate_id():
    return IdNumber.generate_id()


@app.post("/verify_id/", tags=["身份证"], summary="校验身份证")
async def verify_id(id_number):
    '''
    - param id_number: 输入身份证号码
    - return: 错误返回False；正确返回身份证归属地
    '''
    return {"地址": IdNumber.verify_id(id_number),
            "出生日期": "{0}-{1}-{2}".format(id_number[6:10], id_number[10:12], id_number[12:14])}


@app.get("/generate_o_code", tags=["组织机构代码"], summary="生成组织机构代码", response_class=PlainTextResponse)
async def generate_o_code():
    return SocialCredit.create_organizationcode()


@app.post("/verify_o_code/", tags=["组织机构代码"], summary="校验组织机构代码")
async def verify_o_code(o_code):
    '''
    - param o_code:输入组织机构代码
    - return: True or False
    '''
    return {"status": SocialCredit.check_organizationcode(o_code)}


@app.get("/generate_s_code", tags=["统一社会信用代码"], summary="生成统一社会信用代码", response_class=PlainTextResponse)
async def generate_s_code():
    return SocialCredit.create_social_credit()


@app.post("/verify_s_code/", tags=["统一社会信用代码"], summary="校验统一社会信用代码")
async def verify_s_code(s_code):
    '''
    - param s_code: 输入统一社会信用代码
    - return: True or False
    '''
    return {"status": SocialCredit.check_social_credit(s_code)}


@app.post("/summary_week_bugs/", tags=["禅道"], summary="本周bug情况", response_class=PlainTextResponse)
async def summary_week_bugs(
        fileb: UploadFile = File(...),  # UploadFile转为文件对象，可以保存文件到本地
):
    '''
    - param fileb: 上传禅道上导出的bug的csv文件
    - return: 分析结果
    '''
    contents = await fileb.read()
    with open(os.path.join(os.getcwd(), 'zen_tao', fileb.filename), "wb") as f:
        f.write(contents)
    return str(ThisWeekBugsSummary.main(fileb.filename))


@app.get("/summary_all_bugs_weekly/", tags=["禅道"], summary="本周全部项目bug情况")
async def summary_all_bugs_weekly():
    '''
    '本周全部项目bug情况'
    - return: 返回文件，点击下载
    '''
    obj = Runmain()
    obj.run()
    return FileResponse(os.path.join(os.getcwd(), 'zen_tao', 'summary_all_bugs_weekly', 'CountBUGForWeekly.xlsx'),
                        filename='CountBUGForWeekly.xlsx')


@app.post("/summary_version_bugs/", tags=["禅道"], summary="迭代bug情况")
async def summary_version_bugs(
        fileb: UploadFile = File(...),  # UploadFile转为文件对象，可以保存文件到本地
):
    '''
    - param fileb: 上传禅道上导出的bug的csv文件
    - return: 分析结果
    '''
    contents = await fileb.read()
    with open(os.path.join(os.getcwd(), 'zen_tao', fileb.filename), "wb") as f:
        f.write(contents)
    obj = VersionBugsSummary(fileb.filename)
    return {'res': obj.test_results_test()}


@app.get("/summary_version_bugs_file/", tags=["禅道"], summary="下载buglist.csv")
async def summary_version_bugs_file(project_name=None):
    '''
    '先运行迭代bug情况，再下载文件'
    - param project_name: 自定义buglist文件前缀
    - return: 返回文件，点击下载
    '''
    return FileResponse(os.path.join(os.getcwd(), 'zen_tao', 'buglist.csv'), filename=f'{project_name}未关闭buglist.csv')


@app.post("/check_comment/", tags=["禅道"], summary="检查禅道上的bug提示备注是否规范")
async def check_comment(fileb: UploadFile = File(...), ):
    '''
    - param fileb:导入buglist
    - return:返回结果
    '''
    contents = await fileb.read()
    with open(os.path.join(os.getcwd(), 'zen_tao', fileb.filename), "wb") as f:
        f.write(contents)

    obj = CheckBugComment(fileb.filename)
    obj.generate_csv_res()
    return FileResponse(os.path.join(os.getcwd(), 'zen_tao', 'check_comment_result.csv'),
                        filename='check_comment_result.csv')


@app.post("/faker", tags=["faker库生成测试数据"], summary="输入对应的函数名，如 address", response_class=PlainTextResponse)
async def faker_data(para):
    '''
    函数名参考：<a href="https://zhuanlan.zhihu.com/p/87203290" target="view_window">点击跳转</a>
    - param para: 执行的命令，如
    - fake.address()
    - 结果 '香港特别行政区大冶县上街钟街k座 664713'
    - fake.words(nb=3, ext_word_list=None, unique=False)                       # 多个词语
    - 结果 ['选择', '历史', '规定']
    - return: 返回结果
    '''
    fake = Faker(locale='zh_CN')
    return str(eval(para))


@app.post("/compare_2collections/", tags=["数据库"], summary="比较两个mongo同一库不同表数据")
async def compare_2collections(IP_A: IP, IP_B: IP):
    '''
    'change；同一表不同记录数；add：新增表；remove：删除表'
    - param IP_A:第一个ip
    - param IP_B:第二个ip
    - return: 返回结果
    '''
    demo = CompareCollections(IP_A.value, IP_B.value)
    return {"res": demo.main()}


@app.post("/compare_mysql2db/", tags=["数据库"], summary="比较两个mysql相同库里各个表中的数据")
async def compare_mysql2db(IP_A: IP, IP_B: IP, db_name=None):
    '''
    'change；同一表不同记录数；add：新增表；remove：删除表'
    - param IP_A:第一个ip
    - param IP_B:第二个ip
    - param db_name: 默认数据库为yc_gz_case；可以手动输入db名称
    - return: 返回结果
    '''
    demo = CompareMysqlDB(IP_A.value, IP_B.value, db_name)
    if not db_name:
        db_name = 'yc_gz_case'
    return {f"{db_name}": demo.diff_tables()}


@app.get("/repository_branch/", tags=["jenkins"], summary="获取测试环境jenkins中各个仓库的版本号",
         response_class=PlainTextResponse)
async def repository_branch(hostname: IP, command=None):
    '''
    'command是需要执行的命令，默认即可, hostname是要查询的ip，下拉列表选择'
    - param hostname: 选择主机
    - param command: 默认查看jenkins仓库版本号；也可以输入linux命令，如df -h查看磁盘情况
    - return: 返回结果
    '''
    demo = BranchName(command, hostname.value)
    return demo.ssh_client_con()


@app.post("/nginx_format/", tags=["nginx"], summary="nginx.conf格式化")
async def nginx_format(fileb: UploadFile = File(...), ):
    '''
    在线格式化工具：<a href="https://www.dute.org/nginx-config-formatter" target="view_window">点击跳转</a>
    - param fileb:待格式化配置
    - return:格式化后的配置
    '''
    contents = await fileb.read()
    with open(os.path.join(os.getcwd(), 'nginx', fileb.filename), "wb") as f:
        f.write(contents)

    os.system(f'python nginx/nginxfmt.py nginx/{fileb.filename}')
    return FileResponse(os.path.join(os.getcwd(), 'nginx', f'{fileb.filename}'), filename='nginx.conf')


@app.get("/linux_operation/", tags=["运维"], summary="linux的cpu，内存，磁盘使用率统计")
async def linux_operation():
    '''
    统计Linux环境cpu，内存，磁盘使用率
    '''
    obj = LinuxOperation()
    return {'res': obj.analysis()}


@app.get("/ping_linux/", tags=["运维"], summary="ping linux环境", response_class=PlainTextResponse)
async def ping_linux():
    '''
    ping Linux环境
    '''
    obj = PingLinux()
    return str(obj.main())


@app.get("/topN/", tags=["运维"], summary="linux环境硬件使用topN", response_class=PlainTextResponse)
async def topN(hostname: IP, hardware: Hardware):
    '''
    linux环境硬件使用topN
    - hostname:选择IP
    - hardware:选择看cpu还是内存
    '''
    obj = TopN(hostname, hardware)
    return str(obj.get_cmd_result())


@app.get("/service_path/", tags=["运维"], summary="查看执行天网服务的路径", response_class=PlainTextResponse)
async def service_path(hostname: IP):
    '''
    查看执行天网服务的路径
    - hostname:选择IP
    '''
    obj = ServicePath(hostname)
    return ''.join(obj.get_cmd_result())


if __name__ == '__main__':
    uvicorn.run(app='run_byfastapi:app', host="172.30.6.82", port=8001, reload=True, debug=True)
