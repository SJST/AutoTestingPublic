
import time
from pymongo import MongoClient
import json
import re
import os

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
    
    if(remark == '' or remark == 'null'):
        remark = []
    else:
        #    旧版remark，默认是字符串类型
        if(isinstance(remark, (str))):
            remark = [{
                "comment" : remark,
                "date_strf":date_strf,
                "date_string":format_time_string,
                "last_operator":"susan",
                "del_flag":0
            }]
        
        #    新版remark，默认为数组格式
        #    数组中一个文档为一条备注信息
        elif(isinstance(remark, (list))):
            #    旧版remark为空的数据
            if(len(remark) == 0):
                return remark
            else:
                for index, one_remark in enumerate(remark):
                    if('date_strf' not in one_remark.keys()):
                        one_remark.update({'date_strf':date_strf})
                    
                    if('date_string' not in one_remark.keys()):
                        one_remark.update({'date_string':format_time_string})
                        
                    if('last_operator' not in one_remark.keys()):
                        one_remark.update({'last_operator':'susan'})
                        
                    if('del_flag' not in one_remark.keys()):
                        one_remark.update({'del_flag':0})
                    
                    remark[index].update(one_remark)
    
    return remark

#----------------------------------------------------------------------------------------------------------------------

def json_to_mongo(json_data_source_file_path):
    
    success_count = 0
    failed_count = 0
    total_count = 0
    
    models_field_list = ["name", "telephone", "district_city", "province_city", "industry_influence", 
                         "company", "position", "education", "property_direction", "work_experience", 
                         "project_experience", "email", "age", "gender", "address", "skills", 
                         "work_ability", "language_ability", "certificate", "career_intention", 
                         "self_evaluation", "domains", "companycity", "companyaddress", 
                         "personal_profile", "extra_info", "hobby_info", "new_remark", "first_uploader", 
                         "first_upload_time", "last_operator", "update_time", "del_flag", "new_import_flag"]
    
    with open(json_data_source_file_path, "r", encoding="utf-8") as f:     #    , encoding="utf-8"
#         为a+模式时，因为为追加模式，指针已经移到文尾，读出来的是一个空字符串。
#         ftext = f.read()  # 一次性读全部成一个字符串
#         ftextlist = f.readlines() # 也是一次性读全部，但每一行作为一个子句存入一个列表
        
#         json_data_source = f.read()
#         records_obj = re.search(r'^\{\s*"RECORDS"\s*:\s*\[(.*?)\]\s*\}$', json_data_source, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
#         records_json_string = records_obj.group(1)
#         
#         pattern = re.compile(r'{(.*?)}', re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)   # 查找json
#         records_list = pattern.findall(records_json_string)
#         print(type(records_list))
        
        #    eclipse 只能显示300条记录
        data_source_json_list = json.load(f)['RECORDS']
#         print(data_source_json_list)
#         print(type(data_source_json_list))
        
        for one_json_data in data_source_json_list:
            
            insert_data_dict = {}
            
            telephone = ''
            for key in one_json_data:
                value = one_json_data[key]
                
                if key == 'telephone':
                    if value:
                        value = int(value)
                    else:
                        value = int(99999999999)
                    telephone = value
                
                if key == 'new_remark':
                    value = clear_remark(value)
                
                if key in models_field_list:
                    insert_data_dict.update({key: value})
            
            insert_data_dict.update({
                "first_uploader" : "susan",
                "first_upload_time" : format_time_string,
                "last_operator" : "susan",
                "update_time" : format_time_string,
                "del_flag" : 0,
                "new_import_flag" : 1
            })
            
#             ObjectId = candidate_resource.insert(insert_data_dict)
            ObjectId = candidate_resource.update({'telephone':telephone}, {"$set":insert_data_dict}, upsert=True)
            print(ObjectId)
            if ObjectId:
                success_count += 1
            else:
                failed_count += 1
            
            total_count += 1
            
    return {'success_count': success_count, 'failed_count': failed_count, 'total_count': total_count}

#----------------------------------------------------------------------------------------------------------------------

#    程序入口主方法
if __name__ == '__main__':

    #    开发服务器盘符
    data_source_dir = "F:\\ZZMK\\data_source\\"
    
    if not os.path.exists(data_source_dir):
        #    上线服务器盘符
        data_source_dir = "D:\\ZZMK\\data_source\\"

    json_name = "postgre_2018-candidate_resource.json"
    json_data_source_file_path = data_source_dir + json_name
    print(json_data_source_file_path)
    
    result_json = json_to_mongo(json_data_source_file_path)
    print(result_json)








