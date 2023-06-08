#-- coding:UTF-8 --
#!/usr/bin/env python
"""

"""
from dateutil.parser import parse
import csv
from datetime import datetime, timedelta
import time

today_str = time.strftime('%Y-%m-%d', time.localtime(time.time()))
today_datetime = datetime.strptime(today_str, "%Y-%m-%d")
Monday = datetime.strftime(today_datetime - timedelta(today_datetime.weekday()), "%Y%m%d")

def export_csv_file(bug_file):
    with open(bug_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # 过滤这周一之前的bug
        rows = [row for row in reader if (parse(row['创建日期']) - parse(Monday)).days >= 0]
        print(rows)

import os
import sys
#运行目录
CurrentPath = os.getcwd()
print (CurrentPath)
print(os.listdir(CurrentPath))

bug_file = "天罗地网-监委标准版-Bug.csv"
export_csv_file(bug_file)