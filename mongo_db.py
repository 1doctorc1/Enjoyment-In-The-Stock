# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 09:20:52 2022

@author: 张驰
"""

from pymongo import MongoClient
import json
class MyMongoDB:   #创建一个类
    def __init__(self, database, collection):   #利用初始化的方法输入要操作的数据库（database）,集合（collection）
        import pymongo                  #导入pymongo模块
        self.connet = pymongo.MongoClient()   #连接到虚拟机上的mongo数据库
        self.database = self.connet[database] #选择需要操作的数据库名称
        self.collecttion = self.database[collection]   #选择需要操作的集合名称（如果集合名不存在会自动创建）

    def insert(self, data, onlyone=True): #输入需要添加的数据（data），onlyone用来控制增加数据是单条还是多条
        if onlyone:                       #控制数据为单条
            self.collecttion.insert_one(data) #向集合中增加单条数据
        else:                                #否则为多条数据
            self.collecttion.insert_many(data)  #向集合中增加多条数据

    def find(self, query=None, onlyone=True):  #输入查询的条件（query，默认为None指查询全部数据），使用onlyone控制查询的数据是单条还是多条
        if onlyone:                            #默认onlyone为True查询一条数据
            result = self.collecttion.find_one(query)  #将查询的结构用result变量来接收
            return result                    #返回result
        else:                                #onlyone为False查询多条数据
            result = self.collecttion.find(query)        #将查询的结构用result变量来接收
            return list(result)                 #返回result，并转换成列表

    def updata(self, data, new_data, onlyone=True): #指定需要修改的数据（data），修改后的数据（new_data）,onlyone控制修改单条还是多条
        if onlyone:                                 #当onlyone为真
            self.collecttion.update_one(data, {'$set': new_data}) #修改单条数据，使用'$set'表示指定修改数据否则会使数据库中所有数据被新数据覆盖
        else:                                        #当onlyone为假
            self.collecttion.insert_many(data, {'$set': new_data}) #修改多条数据，使用'$set'表示指定修改数据否则会使数据库中所有数据被新数据覆盖

    def delete(self, data, onlyone=True): #删除数据，data需要删除的数据，使用onlyone控制删除的条数
        if onlyone:
            self.collecttion.delete_one(data)  #删除一条
        else:
            self.collecttion.delete_many(data)  #删除多条

# wl = MyMongoDB('stu', 'wl')  #指定我们需要操作的数据库为stu数据库，需要操作的集合为wl集合
# wl.insert([{'name': 'cx', 'profession': 'bigdata', 'age': 18},{'name': 'fhb', 'profession': 'bigdata', 'age': 21}], onlyone=False)
#          #向wl集合中插入两条数据，控制onlyone为False，告知insert函数我们需要插入多条数据

# print(wl.find({'name': 'cx'})) #在inset中为我们已经增加了数据，此时查询名字为cx学生信息并打印

# wl.updata({'profession': 'bigdata'}, {'profession': 'English'}) #将学生专业为大数据的改成英语专业
# print(wl.find(onlyone=False)) #控制onlyone=False，打全部数据

# 本地存储
# 与云端存储仅有链接方式的差别
# def save_figure_to_mongo(data):
#     MONGO_URL="mongodb://localhost:27017/?readPreference=primary&ssl=false&directConnection=true"
#     MONGO_DB='1doctorc1'
#     MONGO_collection1='figure'
#     client=MongoClient(MONGO_URL)
#     db=client[MONGO_DB]
#     if db[MONGO_collection1].insert(data):
#         return True 
#     return False
def save_feedback_to_mongo(data):
    MONGO_URL="mongodb://localhost:27017/?readPreference=primary&ssl=false&directConnection=true"
    MONGO_DB='1doctorc1'
    MONGO_collection2='feedback'
    client=MongoClient(MONGO_URL)
    db=client[MONGO_DB]
    if db[MONGO_collection2].insert_one(data):
        # print("保存成功")
        return True 
    return False
def save_dataframe_to_mongo(data):
    MONGO_URL="mongodb://localhost:27017/?readPreference=primary&ssl=false&directConnection=true"
    MONGO_DB='1doctorc1'
    MONGO_collection3='dataframe'
    client=MongoClient(MONGO_URL)
    db=client[MONGO_DB]
    # """DataFrame类型转化为Bson类型"""
    data=json.loads(data.T.to_json()).values()
    if db[MONGO_collection3].insert_many(data):
        return True 
    return False
# class MongoBase(MongoClient):
#     def __init__(self):
#         self.MONGO_URL="mongodb://localhost:27017/?readPreference=primary&ssl=false&directConnection=true"
#         self.MONGO_DB='1doctorc1'
#         self.MONGO_collection1='figure'
#         self.MONGO_collection2='feedback'
#         self.MONGO_collection3='dataframe'
#         self.client=MongoClient(self.MONGO_DB)
#         self.db=self.client[self.MONGO_DB]
#     def save_feedback_to_mongo(self,data):
#         if self.db[self.MONGO_collection2].insert_one(data):
#             print("保存成功")
#             return True 
#         return False
        
    

















