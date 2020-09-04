
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

collection_data_dict = db.collection_data_dict

def insert_data_dict(collection_name, en_ch_dict):
    filter_dict = {'collection_name': collection_name}
    
    col_list = db.list_collection_names()
    if collection_name in col_list:
      print("数据库存在！")
      collection_data_dict.find_one_and_delete(filter_dict)
    
    insert_dict = {
        'collection_name': collection_name, 'en_ch_dict': en_ch_dict
        }
    
    collection_data_dict.insert_one(insert_dict)
    
    result_dict = collection_data_dict.find_one(filter_dict)
    print(result_dict['en_ch_dict']['telephone'])
    
#     return insert_dict

#----------------------------------------------------------------------------------------------------------------------

#    程序入口主方法
if __name__ == '__main__':
    collection_name = 'candidate_resource'
    en_ch_dict = {
            '_id': 'ID',
            'name': '姓名',
            'telephone': '电话',
            'email': '邮箱',
            'gender': '性别',
            'age': '年龄',
            'education': '教育背景',
            'company': '公司',
            'position': '职位',
            'companycity': '公司所在城市',
            'work_experience': '工作经历',
            'project_experience': '项目经历',
            'extra_info': '额外信息',
            
#             'domains': '领域',
#             'industry_influence': '行业影响力',
#             'province_city': '省市',
#             'district_city': '地区城市',
#             'address': '住址',
#             'companyaddress': '公司所在地址',
#             'property_direction': '业务方向',
#             'career_intention': '职业意向',
#             'work_ability': '工作能力',
#             'skills': '技能',
#             'language_ability': '语言能力',
#             'certificate': '证书',
#             'personal_profile': '个人简介',
#             'self_evaluation': '自我评价',
#             'hobby_info': '兴趣爱好',
            
            'new_remark': '备注',
            
            'first_uploader': '第一位上传简历者',
            'first_upload_time': '第一次上传简历时间',
            'last_operator': '最后操作者',
            'update_time': '最后更新的时间',
            'del_flag': '删除标识',
            'new_import_flag': '新导入标识',
        }
    
    insert_data_dict(collection_name, en_ch_dict)






