#coding=utf-8

from zen_tao.summary_all_bugs_weekly.config import *
from zen_tao.summary_all_bugs_weekly.op_date import *
import xlsxwriter
cn = config()
op_date = op_date()
'''
Create by 古月随笔
'''
class excelchartbyweek(object):
    def __init__(self,xpath):
        self.workbook = xlsxwriter.Workbook(xpath)
    '''
    创建图表图形方法--按周
    '''
    def chart_series_week(self,sheet_name,type,row_len,col_len):
        chart = self.workbook.add_chart({'type': '%s'%(type)})
        if type == "pie":
            for j in range(2,col_len-3):
                chart.add_series({
                    'name':       ['%s'%(sheet_name), 0, j],
                    'categories': ['%s'%(sheet_name), 1, 0, row_len, 0],
                    'values':     ['%s'%(sheet_name), 1, j, row_len,j],
                    'data_labels': {'percentage': 1},   #百分比显示数值
                })
        else:
            for j in range(2,col_len-3):
                chart.add_series({
                    'name':       ['%s'%(sheet_name), 0, j],
                    'categories': ['%s'%(sheet_name), 1, 0, row_len, 0],
                    'values':     ['%s'%(sheet_name), 1, j, row_len,j],#显示数据
                    'data_labels': {'value': 1},#显示数据表
                })
        #添加数据表
        chart.set_table()
        # 设置图表风格.
        chart.set_style(18)
        #设置图表大小
        chart.set_size({'width': 650, 'height': 450})
        return chart

    '''
    创建图表图形方法-按产品或项目
    '''
    def chart_series_all(self,sheet_name,type,row_len,col_len):
        chart = self.workbook.add_chart({'type': '%s'%(type)})
        if type == "pie":
            for j in range(col_len-3,col_len):
                chart.add_series({
                    'name':       ['%s'%(sheet_name), 0, j],
                    'categories': ['%s'%(sheet_name), 1, 0, row_len, 0],
                    'values':     ['%s'%(sheet_name), 1, j, row_len,j],
                    'data_labels': {'percentage': 1},   #百分比显示数值
                })
        else:
            for j in range(col_len-3,col_len):
                chart.add_series({
                    'name':       ['%s'%(sheet_name), 0, j],
                    'categories': ['%s'%(sheet_name), 1, 0, row_len, 0],
                    'values':     ['%s'%(sheet_name), 1, j, row_len,j],#显示数据
                    'data_labels': {'value': 1},#显示数据表
                })
        #添加数据表
        chart.set_table()
        # 设置图表风格.
        chart.set_style(18)
        #设置图表大小
        chart.set_size({'width': 650, 'height': 450})
        return chart

    '''
    柱形图
    ERP&CRMBUG按周统计图
    @sheet_name: Sheet页名称
    @sql_date: 2016-01-04 00:00:00格式
    例:今天为2016-01-04 00:00:00，输入这个时间后，会自动查询2015-12-28 00:00:00---2016-01-03 23:59:59时间段内BUG
    '''
    def CountBUGAsWeeklyForERP(self,sheet_name,sql_date):
        #计算开始时间和结束时间
        dateResult = op_date.week_get(sql_date)
        start_date = dateResult[0][0]
        end_date = dateResult[1][0]
        workbook = self.workbook
        worksheet = self.workbook.add_worksheet(name=sheet_name)
        bold = workbook.add_format({'bold': 1})
        # 定义数据表头列表

        # title = [u'按周统计图', u'统计日期',u'新增', u'已解决',u'已关闭',u'未解决(累计)',u'延期解决(累计)',u'已关闭(累计)',u'总BUG数']
        # buname = [u"ERP2.0(产品)",u"CRM(产品)",u"VMP(产品)"]
        title = cn.bugStatusList
        buname = cn.erpyuvmp_week
        #获取row长度
        row_len = len(buname)
        #获取col长度
        col_len = len(title)
        #定义数据列表
        #ERP统计所有BUG
        data = []
        #添加ERP2.0 BUG数据
        for product_id in cn.erp_pdct_list:
            result = cn.BugCountByProduct(product_id,sql_date)
            data.append(result)

        format_title=workbook.add_format()    #定义format_title格式对象
        format_title.set_border(1)   #定义format_title对象单元格边框加粗(1像素)的格式
        format_title.set_bg_color('#cccccc')   #定义format_title对象单元格背景颜色为
                                               #'#cccccc'的格式
        format_title.set_align('center')    #定义format_title对象单元格居中对齐的格式
        format_title.set_bold()    #定义format_title对象单元格内容加粗的格式


        worksheet.write_row('A1', title, format_title)

        worksheet.write_column('A2', buname,bold)
        for i in range(2,row_len+2):
            worksheet.write_row('B%d'%(i),data[i-2])

        #创建一个图表，类型是column(柱形图)
        chart = self.chart_series_week(sheet_name,"column",row_len,col_len)
        # Add a chart title and some axis labels.
        chart.set_title ({'name': u'按周统计BUG %s--%s'%(start_date,end_date)})
        chart.set_x_axis({'name': u'BUG状态'})
        chart.set_y_axis({'name': u'BUG数'})
        # Insert the chart into the worksheet (with an offset).
        worksheet.insert_chart('A9', chart, {'x_offset': 25, 'y_offset': 10})


        #创建一个图表，类型是column(柱形图)
        chart1 = self.chart_series_all(sheet_name,"column",row_len,col_len)

        # Add a chart title and some axis labels.
        chart1.set_title ({'name': u'按产品或项目统计总BUG %s'%(end_date)})
        chart1.set_x_axis({'name': u'BUG状态'})
        chart1.set_y_axis({'name': u'BUG数'})

        # Insert the chart into the worksheet (with an offset).
        worksheet.insert_chart('L9', chart1, {'x_offset': 25, 'y_offset': 10})

    def teardown(self,xpath):
        self.workbook.close()
        print("报表生成成功,报表所在路径:%s" % (xpath))

if __name__ == "__main__":
    pass

