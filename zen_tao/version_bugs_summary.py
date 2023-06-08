# -- coding:UTF-8 --
import csv
import datetime
import os


class VersionBugsSummary():
    def __init__(self, bug_file):
        # 多次读取csv，是因为多次操作，文件指针有可能在上次操作时，已经指在文件末尾，导致下一次计算结果为空，所以多次读取；且文件不大，不影响性能
        # bug文件名
        self.bug_file = os.path.join(os.getcwd(),'zen_tao' , bug_file)
        # 获取bug总数
        with open(self.bug_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.total_bugs = len([row['Bug编号'] for row in reader])
        # 初始化严重以上、一般和优化bug数
        self.count_veryhigh = self.count_high = self.count_veryhigh_high = self.count_medium = self.count_low = 0
        # 计算已关闭bug数
        self.closed_bugs = 0
        # 计算未关闭bug数
        self.not_closed_bugs = 0
        # 按迭代统计
        self.iteration_bugs = []
        # 获取bug文件里影响版本中的版本名称
        # 按迭代统计用到的字典
        self.dict_list = []
        round_names = self._round_names()
        for round_name in round_names:
            dict = {}
            dict.setdefault("name", round_name)
            dict.setdefault("very_high", 0)
            dict.setdefault("high", 0)
            dict.setdefault("medium", 0)
            dict.setdefault("low", 0)
            dict.setdefault("count", 0)
            self.dict_list.append(dict)
        # 测试轮数，后期根据测试轮数自适应循环和dict
        tmp = [x for x in round_names if '主干(#trunk)' not in x]
        self.rounds = len(tmp)
        # 未关闭分类
        self.not_closed_count_veryhigh = self.not_closed_count_high = self.not_closed_count_medium = self.not_closed_count_low = 0
        # 导出的csv文件名称
        # self.csv_filename = r'buglist' + datetime.datetime.now().strftime(
        #     "%Y%m%d%H%M%S") + '.csv'
        self.csv_filename = os.path.join(os.getcwd(),'zen_tao', 'buglist.csv')

        self.very_high = self.high = self.medium = self.low = self.count = 0


    def _round_names(self):
        with open(self.bug_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            round_names = list(set([row['影响版本'] for row in reader]))
            return round_names

    def bug_level(self):
        with open(self.bug_file, 'r', encoding='utf-8') as f:
            # 已DictReader字典方式读取，方便根据列表然后判断值
            reader = csv.DictReader(f)
            # column = [row['严重程度'] for row in reader]
            # print(column)
            for row in reader:
                # self.round_names[0]提取bug里影响版本，间接提取提测版本，然后计算各个提测版本各个bug级别的个数
                # 这里的循环包括init里的dict都需要根据self.round_names个数添加，这里暂时没想到怎么根据实际自适应
                for dict in self.dict_list:
                    if row['影响版本'] == dict['name']:
                        if row['严重程度'] == '致命':
                            dict['very_high'] = dict['very_high'] + 1
                        if row['严重程度'] == '严重':
                            dict['high'] = dict['high'] + 1
                        if row['严重程度'] == '一般':
                            dict['medium'] = dict['medium'] + 1
                        if row['严重程度'] == '优化':
                            dict['low'] = dict['low'] + 1
                        # count计算的是各个提测版本bug总数
                        dict['count'] = dict['count'] + 1

    def closed_bugs_method(self):
        # 计算已关闭bug的个数
        with open(self.bug_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.closed_bugs = len(
                [row['Bug状态'] for row in reader if row['Bug状态'] == '已关闭'])

    def not_closed_bugs_method(self):
        with open(self.bug_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            tmp_list = [row for row in reader if row['Bug状态'] != '已关闭']
            # 计算未关闭bug的个数
            self.not_closed_bugs = len(tmp_list)
            # print(tmp_list)
            # 根据未关闭bug，提取各个bug级别的个数
            for row in tmp_list:
                if row['严重程度'] == '致命':
                    self.not_closed_count_veryhigh = self.not_closed_count_veryhigh + 1
                if row['严重程度'] == '严重':
                    self.not_closed_count_high = self.not_closed_count_high + 1
                if row['严重程度'] == '一般':
                    self.not_closed_count_medium = self.not_closed_count_medium + 1
                if row['严重程度'] == '优化':
                    self.not_closed_count_low = self.not_closed_count_low + 1

    def export_csv_file(self):
        with open(self.bug_file, 'r', encoding='utf-8') as f:
            # 获取为关闭bug
            reader = csv.DictReader(f)
            tmp_list = [row for row in reader if row['Bug状态'] != '已关闭']
            # 未解决缺陷写进csv文件，, newline='' 写入一行数据后，不空一行
            with open(self.csv_filename, 'w', newline='') as f:
                file_name = [
                    "Bug编号", "所属产品", "分支/平台", "所属模块", "所属迭代", "相关需求", "相关任务",
                    "Bug标题", "关键词", "严重程度", "优先级", "Bug类型", "操作系统", "浏览器",
                    "重现步骤", "Bug状态", "截止日期", "激活次数", "是否确认", "抄送给", "由谁创建",
                    "创建日期", "影响版本", "指派给", "指派日期", "解决者", "解决方案", "解决版本",
                    "解决日期", "由谁关闭", "关闭日期", "重复ID", "相关Bug", "相关用例", "最后修改者",
                    "修改日期", "附件", None
                ]
                # 写入列标题，即DictWriter构造方法的fieldnames参数
                writer = csv.DictWriter(f, fieldnames=file_name)
                writer.writeheader()
                # 多行同时导入
                writer.writerows(tmp_list)
                return f"文件 {self.csv_filename} 导出成功！"

    def round_names_method(self):
        # 总的bug级别个数
        with open(self.bug_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
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

    def test_results_test(self):
        lst_tmp = []
        # 提测轮名称
        lst_tmp.append(self._round_names())
        lst_tmp.append("==================================================")
        # 测试总结
        lst_tmp.append(f"共计 {self.rounds} 轮测试，发现 {self.total_bugs} 个有效问题")
        self.round_names_method()
        lst_tmp.append(f"致命问题：{self.count_veryhigh}个，严重问题：{self.count_high}个")
        lst_tmp.append(
            f"严重级别以上：{self.count_veryhigh_high}个，占比：{self.count_veryhigh_high / self.total_bugs:.1%}"
        )
        lst_tmp.append(
            f"一般问题：{self.count_medium}个，占比：{self.count_medium / self.total_bugs:.1%}"
        )
        lst_tmp.append(
            f"优化问题：{self.count_low}个，占比：{self.count_low / self.total_bugs:.1%}")
        self.closed_bugs_method()
        self.not_closed_bugs_method()
        lst_tmp.append(
            f"截止第 {self.rounds} 轮，已关闭 {self.closed_bugs}，未解决 {self.not_closed_bugs}"
        )
        lst_tmp.append("==================================================")
        # 按迭代统计
        self.bug_level()
        # 计算每个迭代的bug级别及个数
        for dict in self.dict_list:
            lst_tmp.append(dict)
        # 计算每个级别的总个数
        for _ in self.dict_list:
            self.very_high = self.very_high + _['very_high']
            self.high = self.high + _['high']
            self.medium = self.medium + _['medium']
            self.low = self.low + _['low']
            self.count = self.count + _['count']
        lst_tmp.append("==================================================")
        lst_tmp.append(f"致命总数：{self.very_high}； 严重总数：{self.high}； 一般总数：{self.medium}； 优化总数：{self.low}； 总数：{self.count}")
        lst_tmp.append("==================================================")
        # 剩余缺陷各个等级占比和通过率占比
        lst_tmp.append(
            f"致命问题：{self.not_closed_count_veryhigh}个，占比：{self.not_closed_count_veryhigh / self.total_bugs:.1%}"
        )
        lst_tmp.append(
            f"严重问题：{self.not_closed_count_high}个，占比：{self.not_closed_count_high / self.total_bugs:.1%}"
        )
        lst_tmp.append(
            f"一般问题：{self.not_closed_count_medium}个，占比：{self.not_closed_count_medium / self.total_bugs:.1%}"
        )
        lst_tmp.append(
            f"优化问题：{self.not_closed_count_low}个，占比：{self.not_closed_count_low / self.total_bugs:.1%}"
        )
        lst_tmp.append(
            f"已关闭问题：{self.closed_bugs}个，占比：{self.closed_bugs / self.total_bugs:.1%}"
        )
        lst_tmp.append("==================================================")
        lst_tmp.append(self.export_csv_file())
        return lst_tmp


if __name__ == '__main__':
    bug_file = "天罗地网-监委标准版-Bug.csv"
    # bug_file = "天网-烟草标准版-Bug.csv"
    test = VersionBugsSummary(bug_file)
    test.test_results_test()
