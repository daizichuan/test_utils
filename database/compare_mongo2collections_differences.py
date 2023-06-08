# -*- coding: utf-8 -*-
import pymongo
from .utils import compare_datacount
from utils import GetResourceFromMongo

class CompareCollections:
    def __init__(self, IP_A, IP_B):
        obj = GetResourceFromMongo()
        self.data = obj.get_mongodb()

        self.IP_A = self.data[IP_A]
        self.IP_B = self.data[IP_B]

    def get_moongo_datacount(self, data):
        myclient = pymongo.MongoClient(data[0])
        mydb = myclient[data[3]]  # 库名
        mydb.authenticate(data[1], data[2])
        coll_names = mydb.list_collection_names(session=None)  # 获取所有collection
        tmp = {}
        for i in coll_names:
            tmp.setdefault(i, mydb[i].find().count())
        result = {}
        # 按key排序
        for i in sorted(tmp):
            result.setdefault(i, tmp[i])
        # print(result)
        return result

    def main(self):
        first_dict = self.get_moongo_datacount(self.IP_A)
        second_dict = self.get_moongo_datacount(self.IP_B)
        return compare_datacount(second_dict, first_dict)


if __name__ == '__main__':
    demo = CompareCollections()
    demo.main()
