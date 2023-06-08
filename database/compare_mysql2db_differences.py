#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
from .utils import compare_datacount
from utils import GetResourceFromMongo


class CompareMysqlDB():
    def __init__(self, IP_A, IP_B, DB_name=None):
        obj = GetResourceFromMongo()
        self.data = obj.get_mysql()

        if DB_name:
            DB_name = DB_name
        else:
            DB_name = "yc_gz_case"

        self.dict_A = {
            "user": self.data[IP_A]["user"],  # 用户名
            "password": self.data[IP_A]["password"],  # 连接密码
            "host": IP_A,  # 连接地址
            "database": DB_name,  # 数据库名
            "port": self.data[IP_A]["port"]
        }

        self.dict_B = {
            "user": self.data[IP_B]["user"],  # 用户名
            "password": self.data[IP_B]["password"],  # 连接密码
            "host": IP_B,  # 连接地址
            "database": DB_name,  # 数据库名
            "port": self.data[IP_B]["port"]
        }

    # 列出所有的表和记录数
    def list_table(self, dict):
        dict_res = {}
        db = pymysql.connect(**dict)
        cursor = db.cursor()
        cursor.execute("show tables")
        table_list = [tuple[0] for tuple in cursor.fetchall()]
        for _ in table_list:
            cursor.execute(f'select count(*) from `{_}`')
            dict_res[_] = cursor.fetchall()[0][0]
        db.close()
        return dict_res

    def diff_tables(self):
        first_dict = self.list_table(self.dict_A)
        second_dict = self.list_table(self.dict_B)
        return compare_datacount(first_dict, second_dict)


if __name__ == '__main__':
    demo = CompareMysqlDB()
    demo.diff_tables()
