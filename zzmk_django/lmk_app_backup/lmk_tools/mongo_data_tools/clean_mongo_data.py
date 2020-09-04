
import time
from pymongo import MongoClient

#    时间戳
date_strf = time.time()
print(date_strf)
#    格式化时间
format_time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
print(format_time_string)

conn = MongoClient(host="127.0.0.1", port=27017)    #connect to mongodb
db = conn.LMK_DB
candidate_resource = db.candidate_resource

#    统计整个集合的对象数
# print(candidate_resource.count())
    
#    清洗程序，默认remark中只有一条备注信息文档
#    以后如有多条文档，需更改数组下标
def clear_remark(remark):
    
    flag = 0
    if(remark == '' or remark == 'null'):
        #    旧版remark，很多数据起始数据为空，统一成数组格式
        candidate_resource.update({"_id":item['_id']},{"$set":{"new_remark":[]}})
        flag = 1
        
    else:
        #    旧版remark，默认是字符串类型
        if(isinstance(remark, (str))):
            #    把字符串统一格式
#             candidate_resource.update({"_id":item['_id']},{"$set":{"new_remark":[{"comment" : remark}]}})
            candidate_resource.update({"_id":item['_id']},{"$set":{"new_remark":[{
                                                                                  "comment" : remark,
                                                                                  "date_strf":date_strf,
                                                                                  "date_string":format_time_string
                                                                                  }]}})
            flag = 1
        
        #    新版remark，默认为数组格式
        #    数组中一个文档为一条备注信息
        elif(isinstance(remark, (list))):
            #    旧版remark为空的数据
            if(len(remark) == 0):
                return flag
#                 continue
            
            #    清洗数据前期，remark数组中只有一条数据，所以使用下标0
                print(remark[0].keys())
            
            if('date_strf' not in remark[0].keys()):
                candidate_resource.update({"_id":item['_id']},{"$set":{"new_remark.0.date_strf":date_strf}})
                flag = 1
            
            if('date_string' not in remark[0].keys()):
                candidate_resource.update({"_id":item['_id']},{"$set":{"new_remark.0.date_string":format_time_string}})
                flag = 1
    return flag

#----------------------------------------------------------------------------------------------------------------------

#    程序入口主方法
if __name__ == '__main__':
#     for test
#     test_obj = candidate_resource.find({"telephone":15909850681})
#     for item in test_obj:
#         remark = item['new_remark'][0]['date_string']
#         print(remark)
#         candidate_resource.update({"telephone":15909850681, "new_remark.comment":"新进员工王为冬"},{"$set":{"new_remark.$.date_strf":date_strf}})
#     exit(0)
    
#     some_obj = candidate_resource.find({"name":{"$regex":"王为冬"}})
#     print(type(some_obj))
#     #    统计搜索对象数
#     print(some_obj.count())
#     one_obj = candidate_resource.find_one({"name":{"$regex":"王为冬"}})
#     print(type(one_obj))
    all_obj = candidate_resource.find()
    print(all_obj.count())
#     print(type(all_obj))
#     exit(0)
    
    update_count = 0
    for item in all_obj:
        remark = item['new_remark']
        
        flag = clear_remark(remark)
        
        if(flag):
            update_count+=1
    
    print("update_count : " + str(update_count))
