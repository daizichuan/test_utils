#-- coding:UTF-8 --
#!/usr/bin/env python
"""

"""

import pymongo

class GetResourceFromMongo:
    def __init__(self):
        self.Client = pymongo.MongoClient("mongodb://172.30.6.82:27017/")
        self.db = self.Client['IP_Resources']
        self.col = self.db["IP_Resource"]

    def get_ip(self):
        lst = []
        for x in self.col.find({}, {'_id': 0}):
            lst.append(x['IP'])
        return lst

    def get_mongodb(self):
        dict_tmp = {}
        for x in self.col.find({}, {'_id': 0}):
            try:
                if x['mongodb']:
                    dict_tmp[x['IP']] = tuple(x['mongodb'])
            except Exception:
                pass
        return dict_tmp

    def get_mysql(self):
        dict_tmp = {}
        for x in self.col.find({}, {'_id': 0}):
            try:
                if x['mysql']:
                    dict_tmp[x['IP']] = x['mysql']
            except Exception:
                pass
        return dict_tmp

    def get_password(self):
        dict_tmp = {}
        for x in self.col.find({}, {'_id': 0}):
            dict_tmp[x['IP']] = x['password']
        return dict_tmp

    def get_jenkins(self):
        dict_tmp = {}
        for x in self.col.find({}, {'_id': 0}):
            try:
                if x['jenkins']:
                    dict_tmp[x['IP']] = x['jenkins']
            except Exception:
                pass
        return dict_tmp

if __name__ == '__main__':
    obj = GetResourceFromMongo()
    print(obj.get_jenkins())