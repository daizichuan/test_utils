#coding=utf-8
import datetime

from zen_tao.summary_all_bugs_weekly.WeeklyBugCount import *
import os

class Runmain:
    def run(self):
        dateNow = datetime.datetime.now()
        xpath = os.path.join(os.getcwd(), 'zen_tao', 'summary_all_bugs_weekly', 'CountBUGForWeekly.xlsx')
        bugcount = excelchartbyweek(xpath)
        bugcount.CountBUGAsWeeklyForERP("监委烟草本周bug情况",dateNow)
        bugcount.teardown(xpath)

