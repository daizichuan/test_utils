import csv
import pymysql
import re
import os


class DoMysql:
    def __init__(self):
        self.conn = pymysql.connect(host="172.30.6.71",
                                    port=3307,
                                    user="root",
                                    password="",
                                    database="zentao",
                                    charset="utf8")
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()


class CheckBugComment:
    def __init__(self, bug_file):
        self.bug_file = os.path.join(os.getcwd(), 'zen_tao', bug_file)
        self.Nonstandard_total = 0
        self.total = 0
        self.res_name = os.path.join(os.getcwd(), 'zen_tao', 'check_comment_result.csv')
        self.not_match_bugId = []
        self.rows = []

    def export_csv_file(self, bug_file):
        bugId_list = []
        with open(bug_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.rows = [row for row in reader if row['解决方案'] and row['Bug状态'] == '已解决']
            # self.rows = [ row for row in reader ]
            for row in self.rows:
                bugId_list.append(row['Bug编号'])

        self.total = len(bugId_list)
        return bugId_list

    def comment_match(self):
        search_res_list = []
        bugId_list = self.export_csv_file(self.bug_file)
        self.not_match_bugId = bugId_list.copy()

        with DoMysql() as cursor:
            for bug_id in bugId_list:
                sql = f"SELECT objectID as bug_id, actor, REPLACE(`comment`, '\n', ''), CONCAT('http://172.30.6.71:81/zentao/bug-view-',objectID,'.html')  AS bug_url FROM zt_action WHERE objectType = 'bug' and objectID = {bug_id} and `comment` LIKE '%<p>代码信息%'"
                # 执行SQL语句
                cursor.execute(sql)

                res = cursor.fetchall()
                if len(res):
                    search_res_list.append(res)
                    self.not_match_bugId.remove(bug_id)

        return search_res_list

    def comment_not_match(self):
        not_match_bugId_res = []
        for bug_id in self.not_match_bugId:
            bug_name = ''
            bug_creator = ''
            for row in self.rows:
                if int(bug_id) == int(row['Bug编号']):
                    bug_name = row['Bug标题']
                    bug_creator = row['由谁创建']
                    break

            url = f'http://172.30.6.71:81/zentao/bug-view-{bug_id}.html'
            not_match_bugId_res.append(((int(bug_id), bug_name, bug_creator, url),))
        return not_match_bugId_res

    def check_comment(self):
        res_list = []
        search_res_list = self.comment_match()
        for search_res in search_res_list:
            total = len(search_res)
            flag = 0
            for _ in search_res:
                print(_[2])
                if not re.match(r'.*\d+\.\d+.*', _[2], re.S) or 'dev' not in _[2]:
                    flag += 1

            if flag == total:
                bug_name = ''
                bug_creator = ''
                for row in self.rows:
                    if search_res[0][0] == int(row['Bug编号']):
                        bug_name = row['Bug标题']
                        bug_creator = row['由谁创建']
                        break

                res_list.append(((search_res[0][0], bug_name, bug_creator, search_res[0][-1]),))

        self.Nonstandard_total = len(res_list)
        return res_list

    def generate_csv_res(self):
        res_list = []
        res_list_tmp = self.check_comment()
        for _ in res_list_tmp:
            for i in _:
                # print(i)
                res_list.append(i)

        not_match_bugId_res = self.comment_not_match()
        self.comment_not_match()
        for _ in not_match_bugId_res:
            for i in _:
                # print(i)
                res_list.append(i)
        res_list = sorted(res_list)

        headers = ['bug_id', 'bug_name', 'bug_creator', 'bug_url']
        with open(self.res_name, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(res_list)


if __name__ == '__main__':
    obj = CheckBugComment('sss')
    obj.generate_csv_res()
