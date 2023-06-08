from dateutil.parser import parse
import csv
from datetime import datetime, timedelta
import time
import os

class ThisWeekBugsSummary:
    def __init__(self, bug_file):
        self.count_veryhigh_total = self.count_high_total = self.count_veryhigh_high_total = self.count_medium_total = self.count_low_total = self.count_all_total = 0
        self.count_veryhigh_up = self.count_high_up = self.count_veryhigh_high_up = self.count_medium_up = self.count_low_up = self.count_all_up = 0
        self.count_veryhigh_close = self.count_high_close = self.count_veryhigh_high_close = self.count_medium_close = self.count_low_close = self.count_all_close = 0
        self.bug_file = os.path.join(os.getcwd(),'zen_tao' , bug_file)
        # 获取这周一的日期，这周bug从周一开始计算
        today_str = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        today_datetime = datetime.strptime(today_str, "%Y-%m-%d")
        self.Monday = datetime.strftime(today_datetime - timedelta(today_datetime.weekday()), "%Y%m%d")

    def export_csv_file_total(self):
        with open(self.bug_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # 过滤这周一之前的bug
            rows = [row for row in reader if (parse(row['创建日期']) - parse(self.Monday)).days >= 0]
            # print(rows)
            for row in rows:
                if row['严重程度'] == '致命':
                    self.count_veryhigh_total += 1
                if row['严重程度'] == '严重':
                    self.count_high_total += 1
                if row['严重程度'] in ['致命', '严重']:
                    self.count_veryhigh_high_total += 1
                if row['严重程度'] == '一般':
                    self.count_medium_total += 1
                if row['严重程度'] == '优化':
                    self.count_low_total += 1

    def export_csv_file_up(self):
        with open(self.bug_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # 过滤这周一之前的bug
            rows = [row for row in reader if (parse(row['创建日期']) - parse(self.Monday)).days >= 0 and row['Bug状态'] != '已关闭']
            # print(rows)
            for row in rows:
                if row['严重程度'] == '致命':
                    self.count_veryhigh_up += 1
                if row['严重程度'] == '严重':
                    self.count_high_up += 1
                if row['严重程度'] in ['致命', '严重']:
                    self.count_veryhigh_high_up += 1
                if row['严重程度'] == '一般':
                    self.count_medium_up += 1
                if row['严重程度'] == '优化':
                    self.count_low_up += 1

    def export_csv_file_close(self):
        with open(self.bug_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # 过滤这周一之前的bug
            rows = [row for row in reader if (parse(row['创建日期']) - parse(self.Monday)).days >= 0 and row['Bug状态'] == '已关闭']
            # print(rows)
            for row in rows:
                if row['严重程度'] == '致命':
                    self.count_veryhigh_close += 1
                if row['严重程度'] == '严重':
                    self.count_high_close += 1
                if row['严重程度'] in ['致命', '严重']:
                    self.count_veryhigh_high_close += 1
                if row['严重程度'] == '一般':
                    self.count_medium_close += 1
                if row['严重程度'] == '优化':
                    self.count_low_close += 1

    def get_total(self):
        self.export_csv_file_total()
        dic_tmp = {}
        dic_tmp['严重及以上'] = self.count_veryhigh_high_total
        dic_tmp['一般'] = self.count_medium_total
        dic_tmp['优化'] = self.count_low_total
        dic_tmp['总数'] = self.count_veryhigh_high_total + self.count_medium_total + self.count_low_total
        return 'bug总数：' + str(dic_tmp)

    def get_up(self):
        self.export_csv_file_up()
        dic_tmp = {}
        dic_tmp['严重及以上'] = self.count_veryhigh_high_up
        dic_tmp['一般'] = self.count_medium_up
        dic_tmp['优化'] = self.count_low_up
        dic_tmp['总数'] = self.count_veryhigh_high_up + self.count_medium_up + self.count_low_up
        return '未关闭bug：' + str(dic_tmp)

    def get_close(self):
        self.export_csv_file_close()
        dic_tmp = {}
        dic_tmp['严重及以上'] = self.count_veryhigh_high_close
        dic_tmp['一般'] = self.count_medium_close
        dic_tmp['优化'] = self.count_low_close
        dic_tmp['总数'] = self.count_veryhigh_high_close + self.count_medium_close + self.count_low_close
        return '已关闭bug：' + str(dic_tmp)

    def run(self):
        lst = []
        lst.append(self.get_total())
        lst.append(self.get_close())
        lst.append(self.get_up())
        return lst

    @classmethod
    def main(cls, bug_file):
        return cls(bug_file).run()

if __name__ == '__main__':
    pass
    # bug_file = "天罗地网-监委标准版-Bug.csv"
    # ThisWeekBugsSummary().main(bug_file)