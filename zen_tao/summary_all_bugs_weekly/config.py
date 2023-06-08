#coding=utf-8

from zen_tao.summary_all_bugs_weekly.op_date import *
from zen_tao.summary_all_bugs_weekly.op_mysql import *

class config(object):
    def __init__(self):
        self.op_date = op_date()
        # self.ms = op_mysql(host="127.0.0.1",user="root",pwd="",db="zentao")
        self.ms = op_mysql(host="172.30.6.71",user="root",pwd="123456",db="zentao")

    #BUG状态分类:
    bugStatusList = [u'按周统计图', u'统计日期',u'新增', u'已关闭',u'未关闭',u'未关闭(累计)',u'已关闭(累计)',u'总BUG数']

    #同一迭代多个版本或多个项目
    erpyuvmp_week = ['警校比赛平台', '天网-烟草标准版','天罗地网-监委标准版']


    def BugCountByProject(self,projectNo,sql_date):
        ms = self.ms
        data = []
        projectNo = int(projectNo)
        date_result = self.op_date.week_get(sql_date)
        start_date = date_result[0][0]
        end_date = date_result[1][0]
        #查找一个星期内新增的BUG数openedDate 例如今天为2016-01-04 00:00:00，输入这个时间后，会自动查询2015-12-28 00:00:00---2016-01-03 23:59:59时间段内BUG
        AllNewBugCount_OneWeek = "select count(*) from zt_bug where project = '%d' and deleted = '0' and openedDate >= '%s' and openedDate <= '%s'"%(projectNo,start_date,end_date)
        #查找一个星期内已解决的BUG数(以最近的星期天为准，计算星期一到星期天,包含本周 解决到关闭的BUG) resolvedDate
        AllResolvedBugCount_OneWeek = "select count(*) from zt_bug where project = '%d' and deleted = '0' and `status` <> 'active' and resolution <> 'postponed' and resolvedDate >= '%s' and resolvedDate <= '%s'"%(projectNo,start_date,end_date)
        #查找所有未解决BUG数(以最近的星期天为准，计算星期一到星期天)（当前显示BUG状态为未解决的。包含当前还没被解决的、之前遗留的未解决、以及reopen的BUG（累计数据））
        AllNotResolvedBugCount = "select count(*) from zt_bug where project = '%d' and deleted = '0' and `status` =  'active' and openedDate <= '%s'"%(projectNo,end_date)
        #查找用户所有延期解决的问题
        AllPostponedBugCount = "select count(*) from zt_bug where project = '%d' and deleted = '0' and `status` <> 'closed' and resolution = 'postponed' and resolvedDate <= '%s'"%(projectNo,end_date)
        #查找 一个星期内已关闭的BUG数(以最近的星期天为准，计算星期一到星期天) closedDate
        AllClosedBugCount_OneWeek = "select count(*) from zt_bug where project  = '%d' and deleted = '0' and `status` = 'closed' and closedDate >= '%s' and closedDate <= '%s'"%(projectNo,start_date,end_date)

        #查找 已关闭BUG数(累计)
        AllClosedBugCount = "select count(*) from zt_bug where project  = '%d' and deleted = '0' and `status` = 'closed' and closedDate <= '%s'"%(projectNo,end_date)

        #查找 总BUG数
        AllBugCount = "select count(*) from zt_bug where project  = '%d' and deleted = '0' and openedDate <='%s'"%(projectNo,end_date)

        #新增
        dAllNewBugCount_OneWeek = ms.ExecQuery(AllNewBugCount_OneWeek)[0][0]
        #已解决
        dAllResolvedBugCount_OneWeek = ms.ExecQuery(AllResolvedBugCount_OneWeek)[0][0]
        #已关闭
        dAllClosedBugCount_OneWeek = ms.ExecQuery(AllClosedBugCount_OneWeek)[0][0]
        #未解决(累计数据)
        dAllNotResolvedBugCount = ms.ExecQuery(AllNotResolvedBugCount)[0][0]
        #延期解决(累计数据)
        dAllPostponedBugCount = ms.ExecQuery(AllPostponedBugCount)[0][0]
        #已关闭(累计)
        dAllClosedBugCount = ms.ExecQuery(AllClosedBugCount)[0][0]
        #总BUG数
        dAllBugCount = ms.ExecQuery(AllBugCount)[0][0]
        data = ["%s~%s"%(start_date[:-9],end_date[:-9]),dAllNewBugCount_OneWeek,dAllResolvedBugCount_OneWeek,dAllClosedBugCount_OneWeek,dAllNotResolvedBugCount,dAllPostponedBugCount,dAllClosedBugCount,dAllBugCount]
        return data


    def BugCountByProduct(self,productNo,sql_date):
        ms = self.ms
        data = []
        productNo = int(productNo)
        date_result = self.op_date.week_get(sql_date)
        start_date = date_result[0][0]
        end_date = date_result[1][0]
        #查找一个星期内新增的BUG数openedDate 例如今天为2016-01-04 00:00:00，输入这个时间后，会自动查询2015-12-28 00:00:00---2016-01-03 23:59:59时间段内BUG
        AllNewBugCount_OneWeek = "select count(*) from zt_bug where product = '%d' and deleted = '0' and openedDate >= '%s' and openedDate <= '%s'"%(productNo,start_date,end_date)
        #查找 一个星期内已关闭的BUG数(以最近的星期天为准，计算星期一到星期天) closedDate
        AllClosedBugCount_OneWeek = "select count(*) from zt_bug where product  = '%d' and deleted = '0' and `status` = 'closed' and openedDate >= '%s' and openedDate <= '%s'"%(productNo,start_date,end_date)
        #查找一个星期内已解决的BUG数(以最近的星期天为准，计算星期一到星期天) resolvedDate
        AllResolvedBugCount_OneWeek = "select count(*) from zt_bug where product = '%d' and deleted = '0' and `status` <> 'closed' and openedDate >= '%s' and openedDate <= '%s'"%(productNo,start_date,end_date)

        #查找所有未解决BUG数(以最近的星期天为准，计算星期一到星期天)（当前显示BUG状态为未解决的。包含当前还没被解决的、之前遗留的未解决、以及reopen的BUG（累计数据））
        AllNotResolvedBugCount = "select count(*) from zt_bug where product = '%d' and deleted = '0' and `status` =  'active' and openedDate <= '%s'"%(productNo,end_date)
        #查找 已关闭BUG数(累计)
        AllClosedBugCount = "select count(*) from zt_bug where product  = '%d' and deleted = '0' and `status` = 'closed' and openedDate <= '%s'"%(productNo,end_date)
        #查找用户所有延期解决的问题
        AllPostponedBugCount = "select count(*) from zt_bug where product = '%d' and deleted = '0' and `status` <> 'closed' and openedDate <= '%s'"%(productNo,end_date)
        #查找 总BUG数
        AllBugCount = "select count(*) from zt_bug where product  = '%d' and deleted = '0'and openedDate <='%s'"%(productNo,end_date)

        print(AllNewBugCount_OneWeek)
        print(AllResolvedBugCount_OneWeek)
        print(AllClosedBugCount_OneWeek)
        print(AllNotResolvedBugCount)
        print(AllPostponedBugCount)
        print(AllClosedBugCount)
        print(AllBugCount)

        #新增
        dAllNewBugCount_OneWeek = ms.ExecQuery(AllNewBugCount_OneWeek)[0][0]
        #已解决
        dAllResolvedBugCount_OneWeek = ms.ExecQuery(AllResolvedBugCount_OneWeek)[0][0]
        #已关闭
        dAllClosedBugCount_OneWeek = ms.ExecQuery(AllClosedBugCount_OneWeek)[0][0]
        #未解决(累计数据)
        dAllNotResolvedBugCount = ms.ExecQuery(AllNotResolvedBugCount)[0][0]
        #延期解决(累计数据)
        dAllPostponedBugCount = ms.ExecQuery(AllPostponedBugCount)[0][0]
        #已关闭(累计)
        dAllClosedBugCount = ms.ExecQuery(AllClosedBugCount)[0][0]
        #总BUG数
        dAllBugCount = ms.ExecQuery(AllBugCount)[0][0]
        data = ["%s~%s"%(start_date[:-9],end_date[:-9]),dAllNewBugCount_OneWeek,dAllClosedBugCount_OneWeek,dAllResolvedBugCount_OneWeek,dAllPostponedBugCount,dAllClosedBugCount,dAllBugCount]

        return data

    '''
    Product编号:
    '''
    erp_pdct_list = [57, 39, 28]

if __name__ == "__main__":
    pass
    # cn = config()
    # data = []
    # result1 = cn.BugCountByProject(cn.henghawx_pjct,"2016-01-06 00:00:00")
    # data.append(result1)
    # result2 = cn.BugCountByProject(cn.henghash_pjct,"2016-01-06 00:00:00")
    # data.append(result2)
    # result3 = cn.BugCountByProject(cn.henghayy_pjct,"2016-01-06 00:00:00")
    # data.append(result3)
    # print data