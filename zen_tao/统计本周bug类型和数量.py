from dateutil.parser import parse
import csv
from datetime import datetime, timedelta
import time

class Demo:
    def __init__(self, bug_file):
        self.count_veryhigh = self.count_high = self.count_veryhigh_high = self.count_medium = self.count_low = self.count_all = 0
        self.bug_file = bug_file
        # 获取这周一的日期，这周bug从周一开始计算
        today_str = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        today_datetime = datetime.strptime(today_str, "%Y-%m-%d")
        self.Monday = datetime.strftime(today_datetime - timedelta(today_datetime.weekday()), "%Y%m%d")


    def export_csv_file(self):
        with open(self.bug_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # 过滤这周一之前的bug
            rows = [row for row in reader if (parse(row['创建日期']) - parse(self.Monday)).days >= 0]
            # print(rows)
            for row in rows:
                if row['严重程度'] == '致命':
                    self.count_veryhigh = self.count_veryhigh + 1
                if row['严重程度'] == '严重':
                    self.count_high = self.count_high + 1
                if row['严重程度'] in ['致命', '严重']:
                    self.count_veryhigh_high = self.count_veryhigh_high + 1
                if row['严重程度'] == '一般':
                    self.count_medium = self.count_medium + 1
                if row['严重程度'] == '优化':
                    self.count_low = self.count_low + 1

    def __call__(self, *args, **kwargs):
        self.export_csv_file()
        dic_tmp = {}
        dic_tmp['严重及以上'] = self.count_veryhigh_high
        dic_tmp['一般'] = self.count_medium
        dic_tmp['优化'] = self.count_low
        dic_tmp['总数'] = self.count_veryhigh_high + self.count_medium + self.count_low
        print(dic_tmp)

if __name__ == '__main__':
    # bug_file = "天网-烟草标准版-Bug.csv"
    bug_file = "天罗地网-监委标准版-Bug.csv"
    Demo(bug_file)()