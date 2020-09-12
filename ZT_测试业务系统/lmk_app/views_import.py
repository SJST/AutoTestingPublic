
import os
import sys
import importlib
importlib.reload(sys)
from datetime import date
import shutil

import re
import json
import time
from bson.json_util import dumps

try:
    from django.http import JsonResponse
except ImportError:
    from lmk_app_backup import JsonResponse

from django.shortcuts import render, redirect, HttpResponse

# from lmk_app.models import Candidate_user
from lmk_app.models import Candidate_resource
# from lmk_app.models import One_remark, One_prompt

#------------------------------------------

from lmk_app_backup import UserForm
# from .views_mongo import import_one_resume

from lmk_app.lmk_tools.resume_tools.read_file_doc_to_docx import doc_to_docx
from lmk_app.lmk_tools.resume_tools.read_file_word import read_word
from lmk_app.lmk_tools.resume_tools.read_file_pdf import read_pdf

from lmk_app.lmk_tools.resume_tools.resume_name_process import get_candidate_name_from_resume_name
from lmk_app.lmk_tools.resume_tools.resume_format_process import base_symbol_format, date_format_process, module_title_format_process, module_text_format_process, special_format_process

# def personal_base_info(one_module_string):
#     
#     if re.search(r"姓名", one_module_string):
#         name = re.search(r"姓名\s*[:]*\s+([^\s]*)", one_module_string).group(1)
#         print(name)
#         
#     if re.search(r"([男女])", one_module_string):
#         gender = re.search(r"([男女])", one_module_string).group(1)
#         print(gender)
#     
#     if re.search(r"(\d+\s*岁)", one_module_string):
#         age = re.search(r"(\d+\s*岁)", one_module_string).group(1)
#         print(age)
#     elif re.search(r"出生", one_module_string):
#         age = re.search(r"(出生日期|出生年月|生日|年龄)\s*[:]*\s+([^\s]*)", one_module_string).group(2)
#         print(age)
#     
#     if age:
#         age = re.sub("\s+", "", age, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
#         age = re.search(r"^(\d{2,4}[年]*)", age).group(1)
#     
#     if re.search(r"(联系方式|电话)\s*[:\s]\s*(\d{11})", one_module_string):
#         telephone = re.search(r"(联系方式|电话)\s*[:\s]\s*(\d{11})", one_module_string).group(2)
#         print(telephone)
#     elif re.search(r"(\s*\d{11}\s*)", one_module_string):
#         telephone = re.search(r"\s*(\d{11})\s*", one_module_string).group(1)
#         print(telephone)
#     
#     if re.search(r"邮箱|email", one_module_string):
#         email = re.search(r"(邮箱|email)\s*[:]*\s+([^\s]*)", one_module_string).group(2)
#         print(email)
#     elif re.search(r"\s+[^\s+]*\@[^\.]*\.[^\s+]*\s+", one_module_string):
#         email = re.search(r"\s+([^\s+]*\@[^\.]*\.[^\s+]*)\s+", one_module_string).group(1)
#         print(email)
#     
#     if re.search(r"学历|统招|本科|博士|硕士|双学位|学士学位|专科|大专|大学", one_module_string):
#         if re.search(r"学历\s*[:]*\s+([^\s]*)", one_module_string):
#             education  = re.search(r"学历\s*[:]*\s+([^\s]*)", one_module_string).group(1)
#         else:
#             education  = re.search(r"([^\s^\(\)]*(统招|本科|博士|硕士|双学位|学士学位|专科|大专|大学)[^\s^\(^\)]*)", one_module_string).group(1)
#         
#         print(education)
#     
#     if re.search(r"(当前职位|当前职位及职级)\s*[:\s]\s*(.*)$", one_module_string):
#         position_rank = re.search(r"(当前职位|当前职位及职级)\s*[:\s]\s*(.*)$", one_module_string).group(2)
#         print(position_rank)


#    简历导入    基本路径
#    开发服务器盘符
resume_base_dir = "F:\\ZZMK\\imported_resume\\"
# #    上线服务器盘符
# resume_base_dir = "D:\\ZZMK\\imported_resume\\"

if not os.path.exists(resume_base_dir):
    resume_base_dir = "D:\\ZZMK\\imported_resume\\"

source_file_string = "source_file\\"
target_txt_file_string = "target_txt_file\\"
#    汇总所有，所有的源文件与目标文件放在一起
collect_dir = "all_collect\\"

#    **************************************************************
#    模块分离
def module_separation(all_text, resume_user_dir, resume_name):
    all_text = special_format_process(all_text)
        
    all_text = base_symbol_format(all_text)
    
    all_text = re.sub(r"(\d)\s*\)", r"\1)", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    
    all_text = date_format_process(all_text)
    
    all_text = re.sub(r"·{1,}", r"\t", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    
    all_text = re.sub(r"项目经验\s*", r"项目经验 \n", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    
#     resume_user_dir = 'F:\\ZZMK\\imported_resume\\susan\\'
    login_name = re.search(r"\\([^\\]*)\\$", resume_user_dir).group(1)
    print(login_name)
    
    filter_params_dict = {}
    update_params_dict = {}
    
    name = get_name(resume_name, all_text)
    
    telephone = get_telephone(all_text)
#     
#     try:
#         telephone = get_telephone(all_text)
#     except ValueError:
#         if not telephone:
#             print("not telephone")
#             status = 'failed'
#             return status
    

    
    email = get_email(all_text)
    education = get_education(all_text)
    
    gender = get_gender(all_text)
    age = get_age(all_text)
    position_rank = get_position_rank(all_text)
    district_city = get_district_city(all_text)
    
    update_params_dict.update({
                    'name': name, 'gender': gender, 'age': age, 'email': email, 
                    'education': education, 'position': position_rank, 'district_city': district_city
                    })
    
    #    获取其他字段内容
    update_params_dict = get_other_params(all_text, update_params_dict)
    
    work_experience = ''
    if 'work_experience' in update_params_dict:
        work_experience = update_params_dict['work_experience']
    
    for key in update_params_dict:
        
        if key != 'work_experience':
            if key != 'district_city':
                work_experience = work_experience.replace(update_params_dict[key], "", re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
            
#             print(key + "\n")
#             print(update_params_dict[key] + "\n")
        
#     print(work_experience)
    update_params_dict.update({'work_experience': work_experience})
    
    filter_params_dict.update({'telephone': telephone})
    
    exist_obj = Candidate_resource.objects(telephone=telephone).as_pymongo()
    if not exist_obj:
        #    格式化时间
        format_time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        update_params_dict.update({'first_uploader': login_name, 'first_upload_time': format_time_string})
        update_params_dict.update({'last_operator': login_name, 'update_time': format_time_string})
        update_params_dict.update({'new_import_flag': 1})
    else:
        format_time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        update_params_dict.update({'last_operator': login_name, 'update_time': format_time_string})
        update_params_dict.update({'new_import_flag': 0})
    
    candidate_obj = Candidate_resource.objects(**filter_params_dict).update(upsert= True, **update_params_dict)
    
    if candidate_obj:
        status = 'success'
        
        once_imported_telephone_list_file = 'once_imported_telephone_list.txt'
        once_imported_telephone_list_file_path = resume_user_dir + once_imported_telephone_list_file
        if os.path.exists(once_imported_telephone_list_file_path):
            with open(once_imported_telephone_list_file_path, "a") as f:     #    , encoding="utf-8"
                f.write(telephone + ',')
    else:
        status = 'failed'

    return status

#    **************************************************************

def get_name(input_txt_name, one_module_string):
    
    name = ''
    name_from_file_name = get_candidate_name_from_resume_name(input_txt_name)
    if re.search(r"姓\s*名", one_module_string):
        name = re.search(r"姓\s*名\s*[:]*\s*([^\s]*)", one_module_string).group(1)
        
        if name != name_from_file_name:
            print(name + 'diffirent' + name_from_file_name)
#             name = name_from_file_name
    
    if not name:
        name = name_from_file_name
    
#     if name:
#         print(name)
    
    return name

def get_telephone(one_module_string):
    telephone = ''
    if re.search(r"(联系方式|电话|手机|手机号码|Mobile)\s*[:\s]\s*(\d{3}\s*-{0,1}\s*\d{4}\s*-{0,1}\s*\d{4})", one_module_string):
        telephone = re.search(r"(联系方式|电话|手机|手机号码|Mobile)\s*[:\s]\s*(\d{3}\s*-{0,1}\s*\d{4}\s*-{0,1}\s*\d{4})", one_module_string).group(2)
#         print(telephone)
    elif re.search(r"(\s*\d{3}\s*-{0,1}\s*\d{4}\s*-{0,1}\s*\d{4}\s*)", one_module_string):
        telephone = re.search(r"\s*(\d{3}\s*-{0,1}\s*\d{4}\s*-{0,1}\s*\d{4})\s*", one_module_string).group(1)
#         print(telephone)
    
    if telephone:
        telephone = re.sub("-", "", telephone, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
        telephone = re.sub("\s+", "", telephone, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
#         print(telephone)
        
    return telephone

def get_email(one_module_string):
    email = ''
    if re.search(r"邮箱|e[-_]*mail", one_module_string):
        if re.search(r"(邮箱|e[-_]*mail)\s*[:：]*\s*[^\s]*\@[^\.]*\.[^\s]*\s+", one_module_string):
            email = re.search(r"(邮箱|e[-_]*mail)\s*[:：]*\s*([^\s:]*\@[^\.]*\.[^\s]*)\s+", one_module_string).group(2)
#         print(email)
    elif re.search(r"\s+[^\s]*\@[^\.]*\.[^\s]*\s+", one_module_string):
        email = re.search(r"\s+([^\s]*\@[^\.]*\.[^\s]*)\s+", one_module_string).group(1)
#         print(email)
    else:
        print("no email info")
    
    if email:
        email = re.sub("\s+", "", email, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
#         print(email)
    return email

def get_education(one_module_string):
    education = ''
    if re.search(r"学历|统招|本科|博士|硕士|双学位|学士学位|专科|大专|大学", one_module_string):
        if re.search(r"学历\s*[:][^\n]*([^\s]*)", one_module_string):
            education  = re.search(r"学历\s*[:]*\s+([^\s]*)", one_module_string).group(1)
#             one_module_string = re.sub(r"学历\s*[:]*\s+([^\s]*)", "", one_module_string)
        elif re.search(r"教育经历\s*[:\s]([^\n]*)\n", one_module_string):
            temp_edu = re.search(r"教育经历\s*[:\s]([^\n]*)\n", one_module_string).group(1)
            
            if re.search(r"学历|统招|本科|博士|硕士|双学位|学士学位|专科|大专|大学", temp_edu):
                education  = re.search(r"([^\s^\(^\)^,^。]*(统招|本科|博士|硕士|双学位|学士学位|专科|大专|大学)[^\s^\(^\)^,^。]*)", temp_edu).group(1)
            else:
                education  = re.search(r"([^\s^\(^\)^,^。]*(统招|本科|博士|硕士|双学位|学士学位|专科|大专|大学)[^\s^\(^\)^,^。]*)", one_module_string).group(1)
        else:
            education  = re.search(r"([^\s^\(^\)^,^。]*(统招|本科|博士|硕士|双学位|学士学位|专科|大专|大学)[^\s^\(^\)^,^。]*)", one_module_string).group(1)
#             one_module_string = re.sub(r"^.*?([^\s^\(\)]*(统招|本科|博士|硕士|双学位|学士学位|专科|大专|大学)[^\s^\(^\)]*).*?$", "", one_module_string, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
#         print(education)
    
#     if education:
#         print(education)
    return education

def get_other_params(all_text, update_params_dict):
    
#     education = update_params_dict['education']
    education = ''
    work_experience = ''
    temp_education = ''
    
    all_text = re.sub(r"(\d)\n", r"\1@@@\n", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub(r"@@@", "", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    
    format_flag = 0
    if re.search(r"\n([^\n]*(20\d{2}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*[\s\-~至—]{1,2}\s*(20\d{2}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*|至今))[^\n]*)", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M):
        
        format_flag = 1
        
        all_text = re.sub(r"\n([^\n]*(20\d{2}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*[\s\-~至—]{1,2}\s*(20\d{2}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*|至今))[^\n]*)", r"###\n\1", all_text)
#         print(all_text)
        all_module_list = list(all_text.split("###"))
#         print(all_module_list)
          
        for one_module_string in all_module_list:
#             print("\n")
            
            if re.search(r"(^[^\n]*(\d{4}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*[\s\-~至—]{1,2}\s*(\d{4}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*|至今))[^\n]*).*$", one_module_string, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M):
                module_obj = re.search(r"(^[^\n]*(\d{4}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*[\s\-~至—]{1,2}\s*(\d{4}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*|至今))[^\n]*)(.*$)", one_module_string, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
                
                title_text = module_obj.group(0)
                
                temp_dict = get_params_from_standard_formart(title_text, update_params_dict, format_flag)
                
                update_params_dict = temp_dict['update_params_dict']
                
                title_text = temp_dict['text']
                title_text = module_text_format_process(title_text)
                
                title_text_obj = re.search(r"(^[^\n]*(\d{4}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*[\s\-~至—]{1,2}\s*(\d{4}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*|至今))[^\n]*)(.*$)", title_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
                
                #---
                one_module_title = title_text_obj.group(1)
#                     one_module_text = module_obj.group(0)
                one_module_text = title_text_obj.group(4)
                
                one_module_title = module_title_format_process(one_module_title)
                
                if re.search(r"(教育经历|大学院{0,1}|学院|学历|统招|本科|博士|硕士|双学位|学士(学位){0,1}|专科|大专)", one_module_title, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M):
                    temp_education += one_module_title + "\n"
                    continue
                
                one_module_text = module_text_format_process(one_module_text)
                #---
                
                work_experience += one_module_title + "\n" + one_module_text + "\n"
                work_experience = re.sub(r"###.*###", "", work_experience, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
                work_experience = re.sub(r"###", "", work_experience, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
            
        if temp_education:
            temp_education = re.sub(r"教育经历[\s:]", "", temp_education, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
            temp_education = re.sub(r"^\s+|\s+$", "", temp_education, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
            update_params_dict.update({'education': temp_education})
        
        work_experience = re.sub(r"教育经历[\s:：]*", "", work_experience, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
        work_experience = re.sub(r"\n{1,}", "\n", work_experience, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
        
        update_params_dict.update({'work_experience': work_experience})
        
    else:
        print('not in') #    进入另一种模式，匹配原始标准的正则表达式
        temp_dict = get_params_from_standard_formart(all_text, update_params_dict, format_flag)
        update_params_dict = temp_dict['update_params_dict']
        
    return update_params_dict

def get_gender(one_module_string):
    gender = ''
    if re.search(r"\s([男女])\s", one_module_string):
        gender = re.search(r"\s([男女])\s", one_module_string).group(1)
    elif re.search(r"\([^\)]*([男女])[^\)]*\)", one_module_string):
        gender = re.search(r"\([^\)]*([男女])[^\)]*\)", one_module_string).group(1)
        
#     if gender:
#         print(gender)
    return gender

def get_age(one_module_string):
    age = ''
    if re.search(r"(\d+\s*岁)", one_module_string):
        age = re.search(r"(\d+\s*岁)", one_module_string).group(1)
#         print(age)
    elif re.search(r"(出生日期|出生年月{0,1}|生日)", one_module_string):
#         age = re.search(r"(出生日期|出生年月|生日|年龄)\s*[:]*\s*(\d{2,4}\s*[年\.\-\/]\s*\d{1,2}\s*[月\.\-\/]*\s*(\d{1,2}日{0,1}){0,1})", one_module_string).group(2)
        age = re.search(r"(出生日期|出生年月{0,1}|生日)\s*[:]*\s*(\d{2,4}\s*([年\.\-\/]\s*\d{1,2}\s*[月\.\-\/]*\s*(\d{1,2}日{0,1}){0,1}){0,1})", one_module_string).group(2)
#         print(age)
    elif re.search(r"年{0,1}\s*龄\s*[:]*\s*(\d{2,4}(年|岁){0,1})", one_module_string):
        age = re.search(r"年{0,1}\s*龄\s*[:]*\s*(\d{2,4}(年|岁){0,1})", one_module_string).group(1)
        
    elif re.search(r"[男女]\s+(\d{2,4}\s*(年|岁){0,1})", one_module_string):
        age = re.search(r"[男女]\s+(\d{2,4}\s*(年|岁){0,1})", one_module_string).group(1)
        
    if age:
        age = re.sub("\s+", "", age, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
        if re.search(r"^(\d{2,4}[年]*)", age):
            age = re.search(r"^(\d{2,4}[年]*)", age).group(1)
    
#     if age:
#         print(age)
    return age

def get_position_rank(one_module_string):
    position_rank = ''
    if re.search(r"(当前职位|当前职位及职级)\s*[:\s]\s*(.*)$", one_module_string, re.RegexFlag.I|re.RegexFlag.M):
        position_rank = re.search(r"(当前职位|当前职位及职级)\s*[:\s]\s*(.*)$", one_module_string, re.RegexFlag.I|re.RegexFlag.M).group(2)
#         print(position_rank)
    
#     if position_rank:
#         print(position_rank)
    return position_rank

def get_district_city(one_module_string):
    district_city = ''
    
    if re.search(r"(出生地|户籍|地点|所在地|工作地|居住地|工作地区|定位)\s*[:\s]([^\n]*)\n", one_module_string):
        temp_city = re.search(r"(出生地|户籍|地点|所在地|工作地|居住地|工作地区|定位)\s*[:\s]([^\n]*)\n", one_module_string).group(2)
        district_city = re.search(r"\s*([^\s]*市{0,1})\s*", temp_city).group(1)
    
    elif re.search(r"\s([^\s]*市)\s", one_module_string):
        district_city = re.search(r"\s([^\s]*市)\s", one_module_string).group(1)
    
    elif re.search(r"\s([^\s]*市[^\s]*区[^\s]*)\s", one_module_string):
        district_city = re.search(r"\s([^\s]*市[^\s]*区[^\s]*)\s", one_module_string).group(1)
        
    elif re.search(r"[\s\(\,]((北京|上海|沈阳|大连))[\s\)\,]", one_module_string):
        district_city = re.search(r"[\s\(\,]((北京|上海|沈阳|大连))[\s\)\,]", one_module_string).group(1)
#         print(district_city)
    
#     if district_city:
#         print(district_city)
    return district_city

def get_params_from_standard_formart(text, update_params_dict, format_flag):
    
    #    处理工作经历中，掺杂的其他字段的信息。
                 
    #    个人信息/个人资料/基本信息/基本资料
    personal_base_info_list = ["个人信息","个人资料","基本信息","基本资料"]
    #    个人简介
    profile_info_list = ["个人简介"]
    #    联系方式
    contact_info_list = ["联系方式"]
    #    当前职位及职级    current_position_rank_list
    current_position_rank_list = ["当前职位及职级","当前职位","当前职级"]
    #    教育背景/教育经历
    education_info_list = ["教育背景","教育经历"]
    #    工作经历/工作经验
    work_experience_info_list = []  #    ["工作经历","工作经验","职业经历"]
    #    项目经验/项目经历
    project_experience_info_list = []     #    ["项目经历","项目经验"]  #    "主要项目经验",
    
    if not format_flag:
        work_experience_info_list = work_experience_info_list + ["工作经历","职业经历"]
    else:
        project_experience_info_list = project_experience_info_list + ["项目经历","项目经验"]   
         
    #    工作能力标签/工作能力/专业评价
    ability_info_list = ["工作能力","专业评价","工作能力标签"]
    #    语言能力
    language_info_list = ["语言能力","外语水平"]   #    ,"工作语言"
    #    证书
    certificate_info_list = ["奖励及证书","证书"]
    #    专业技能/技能标签/技能评价/IT技能
    skill_info_list = ["专业技能","技能评价","技能标签","IT技能","个人技能","我的技能","熟练使用","熟练操作"]
    #    求职信息/求职意向/职业意向
    intention_info_list = ["求职信息","求职意向","职业意向"]
    #    自我评价
    self_evaluation_info_list = ["自我评价","自我描述"]
    #    附加信息
    extra_info_list = ["附加信息","个人荣誉","附:"]
    #    兴趣爱好
    hobby_info_list = ["兴趣爱好","爱好","爱好及特长"]
     
    sub_all_module_title_info_list = [personal_base_info_list, profile_info_list, contact_info_list, 
                                  current_position_rank_list, education_info_list, work_experience_info_list, 
                                  project_experience_info_list, ability_info_list, language_info_list, 
                                  certificate_info_list, skill_info_list, intention_info_list, 
                                  self_evaluation_info_list, extra_info_list, hobby_info_list]
    
    sub_all_module_title_info_string_list = (personal_base_info_list + profile_info_list + contact_info_list + 
                         current_position_rank_list + education_info_list + 
                         work_experience_info_list + project_experience_info_list + 
                         ability_info_list + language_info_list + certificate_info_list + 
                         skill_info_list + intention_info_list + 
                         self_evaluation_info_list + extra_info_list + hobby_info_list)
    
    if re.search(r"教育经历\s*项目经验", text):
        text = re.sub(r"\s*教育经历\s*项目经验", r"\n项目经验", text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    
    for one_info_list in sub_all_module_title_info_list:
        for one_string in one_info_list:
            pattern = one_string + r'[\s:]'
            regex = re.compile(pattern)
            
            if regex.findall(text):
                text = re.sub(one_string, "###" + one_string, text)
                continue
     
    sub_all_module_list = list(text.split("###"))
    
    normal_module_dict = {}
    
    for temp_one_module_string in sub_all_module_list:
        if re.search(r"^\s*([^:^\s]*)[:\s]\s*(.*)$", temp_one_module_string, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M):
            temp_module_obj = re.search(r"^\s*([^:^\s]*)[:\s]\s*(.*)$", temp_one_module_string, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
            
            temp_module_del_text = temp_module_obj.group(0)
            temp_one_module_title = temp_module_obj.group(1)
            temp_one_module_text = temp_module_obj.group(2)
            
            temp_one_module_title = re.sub(r"^\s+|\s+$", "", temp_one_module_title, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
            temp_one_module_text = re.sub(r"^\s+|\s+$", "", temp_one_module_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
            
            if temp_one_module_title in sub_all_module_title_info_string_list:
                
                normal_module_dict[temp_one_module_title] = temp_one_module_text
                
                text = text.replace(temp_module_del_text, "")
            
        else:
            continue
    
    for temp_module_title in normal_module_dict:
        temp_module_text = normal_module_dict[temp_module_title]
        
        temp_module_text = re.sub("^\s*ABOUT\s*ME\s*", "", temp_module_text)
        temp_module_text = re.sub("^\s*EDUCATION\s*", "", temp_module_text)
        temp_module_text = re.sub("^\s*WORKEXPERIENCE\s*", "", temp_module_text)
        temp_module_text = re.sub("^\s*PROJECTEXPERIENCE\s*", "", temp_module_text)
        temp_module_text = re.sub("^\s*SKILL\s*", "", temp_module_text)
        
        temp_module_text = re.sub(r"^\s+|\s+$", "", temp_module_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
        temp_module_text = re.sub(r"^:$", "", temp_module_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
        
        if temp_module_text:
            if temp_module_title in current_position_rank_list:
                update_params_dict.update({'position': temp_module_text})
            elif temp_module_title in education_info_list:
                if len(re.findall(".*?\n", temp_module_text)) > 4:
                    temp_module_text = re.search(r"(([^\n]*\n){0,4})", temp_module_text).group(1)
                
                update_params_dict.update({'education': temp_module_text})
            elif temp_module_title in work_experience_info_list:
                update_params_dict.update({'work_experience': temp_module_text})
            elif temp_module_title in project_experience_info_list:
                update_params_dict.update({'project_experience': temp_module_text})
            elif temp_module_title in skill_info_list:
                update_params_dict.update({'skills': temp_module_text})
            
            elif temp_module_title in profile_info_list:
                update_params_dict.update({'personal_profile': temp_module_text})
            elif temp_module_title in ability_info_list:
                update_params_dict.update({'work_ability': temp_module_text})
            elif temp_module_title in language_info_list:
                update_params_dict.update({'language_ability': temp_module_text})
            elif temp_module_title in certificate_info_list:
                update_params_dict.update({'certificate': temp_module_text})
            elif temp_module_title in intention_info_list:
                update_params_dict.update({'career_intention': temp_module_text})
            elif temp_module_title in self_evaluation_info_list:
                update_params_dict.update({'self_evaluation': temp_module_text})
            elif temp_module_title in extra_info_list:
                update_params_dict.update({'extra_info': temp_module_text})
            elif temp_module_title in hobby_info_list:
                update_params_dict.update({'hobby_info': temp_module_text})
    
    temp_dict = {
                        'update_params_dict': update_params_dict,
                        'text': text
                    }
        
    return temp_dict
 
#    **************************************************************

#    在上传完简历之后，在上传按钮的下部，显示当次导入简历的信息列表
def after_upload_resume(request):
    
    login_name = request.session.get('login_name')
    login_name = login_name + "\\"
    
    resume_user_dir = resume_base_dir + login_name
    once_imported_telephone_list_file = 'once_imported_telephone_list.txt'
    once_imported_telephone_list_file_path = resume_user_dir + once_imported_telephone_list_file
    
    with open(once_imported_telephone_list_file_path, "r") as f:     #    , encoding="utf-8"
        telephone_string = f.read()
    
    telephone_string = re.sub(r',$', '', telephone_string, re.RegexFlag.S|re.RegexFlag.M)
    telephone_string = re.sub(r'^\s+|\s+$', '', telephone_string, re.RegexFlag.S|re.RegexFlag.M)
    
    if telephone_string:
        telephone_list = telephone_string.split(',')
        
        if telephone_list:
            telephone_list = list(map(int, telephone_list))
            
            candidate_obj = Candidate_resource.objects(telephone__in=telephone_list).as_pymongo()
            
            result_json = dumps(candidate_obj, ensure_ascii=False)
#             print(result_json)
            return HttpResponse(result_json)
    else:
        return HttpResponse({'msg':'failed'})
    
    
    

    

#    **************************************************************

#    在上传简历之前，创建记录用户当次上传文件的telephone
def before_upload_resume(request):
    
    login_name = request.session.get('login_name')
    login_name = login_name + "\\"
    
    resume_user_dir = resume_base_dir + login_name
    once_imported_telephone_list_file = 'once_imported_telephone_list.txt'
    once_imported_telephone_list_file_path = resume_user_dir + once_imported_telephone_list_file
    
#     # 如果写入文件存在，则清空文件或者删除文件
#     if os.path.exists(once_imported_telephone_list_file_path):
#         os.remove(once_imported_telephone_list_file_path)
#         print('exist and remove')
    
    open(once_imported_telephone_list_file_path, "w")
    
    if os.path.exists(once_imported_telephone_list_file_path):
        status = 'success'
    else:
        status = 'failed'
    
    print('once_imported_telephone_list.txt mkdir ' + status)
    return JsonResponse({'status': status})

#    简历导入
def resume_import(request):
    
    session_name = request.session.get('login_name')
    login_name = session_name + "\\"
    
    #    格式化时间
    format_time_string = time.strftime('%Y-%m-%d_%H-%M', time.localtime())
    time_string = format_time_string + "\\"
    
    #    F:\ZZMK\imported_resume\susan\
    resume_user_dir = resume_base_dir + login_name
    if not os.path.exists(resume_user_dir):
        os.mkdir(resume_user_dir)
    
#     #    F:\ZZMK\imported_resume\susan\2019-01-01_23-08\
#     if not os.path.exists(resume_user_dir + time_string):
#         os.mkdir(resume_user_dir + time_string)
#     
#     #    F:\ZZMK\imported_resume\susan\2019-01-01_23-08\target_txt_file
#     if not os.path.exists(resume_user_dir + time_string + target_txt_file_string):
#         os.mkdir(resume_user_dir + time_string + target_txt_file_string)
    
    if request.method == 'POST':
        userform = UserForm(request.POST, request.FILES)
        
        resume_file = request.FILES.get("upload", None)    # 获取上传的文件，如果没有文件，则默认为None
        
        if resume_file:
            
            resume_name = resume_file.name
            
            resume_name = re.sub(r'[【】（）]', ' ', resume_name, re.RegexFlag.S|re.RegexFlag.M)
            resume_name = re.sub(r'^\s+|\s+$', '', resume_name, re.RegexFlag.S|re.RegexFlag.M)
            
            file_name = resume_name
            
            file_name = re.sub(r'\..*$', '', file_name, re.RegexFlag.S|re.RegexFlag.M) + "\\"
            
            #    F:\ZZMK\imported_resume\susan\【产品运营】张娅飞 商业\source_file\产品运营 张娅飞 商业.docx
            resume_name_dir = resume_user_dir + file_name
            
            source_file_dir = resume_name_dir + source_file_string
            source_file_path = source_file_dir + resume_name
            print("target_txt_file_path:" + source_file_path)
            
            #    F:\ZZMK\imported_resume\susan\产品运营 张娅飞 商业\target_txt_file\产品运营 张娅飞 商业.txt
            target_txt_file_dir = resume_name_dir + target_txt_file_string
            target_txt_file_path = target_txt_file_dir + resume_name
            target_txt_file_path = re.sub(r'\..*$', '', target_txt_file_path, re.RegexFlag.S|re.RegexFlag.M) + ".txt"
            print("target_txt_file_path:" + target_txt_file_path)
            
            #    F:\ZZMK\imported_resume\susan\产品运营 张娅飞 商业\
            if not os.path.exists(resume_name_dir):
                os.mkdir(resume_name_dir)
            
            #    F:\ZZMK\imported_resume\susan\产品运营 张娅飞 商业\source_file\
            if not os.path.exists(source_file_dir):
                os.mkdir(source_file_dir)
            
            #    F:\ZZMK\imported_resume\susan\产品运营 张娅飞 商业\target_txt_file\
            if not os.path.exists(target_txt_file_dir):
                os.mkdir(target_txt_file_dir)
            
            #    读取用户上传的文件，写入本地
            with open(source_file_path, 'wb+') as one_resume:
                for chunk in resume_file.chunks():
                    one_resume.write(chunk)
        
            if os.path.exists(source_file_path):
                
                if(re.search('\.doc$', source_file_path)):
                    new_source_file_path = re.sub(r'\.doc$', '.docx', source_file_path)
                    doc_to_docx(source_file_path, new_source_file_path)
                    source_file_path = new_source_file_path
                    
                    if os.path.exists(source_file_path):
                        read_word(source_file_path, target_txt_file_path)
                    
                #    简历格式大致分为，doc，docx，pdf，三种默认格式
                if(re.search('\.docx$', source_file_path)):
                    #    处理本地的简历文件，转换成txt文件
                    read_word(source_file_path, target_txt_file_path)
                elif(re.search('\.pdf$', source_file_path)):
                    read_pdf(source_file_path, target_txt_file_path)
                
                
                resume_collect_dir = resume_base_dir + collect_dir
                
                if os.path.exists(target_txt_file_path):
                    if not os.path.exists(resume_collect_dir):
                        os.mkdir(resume_collect_dir)
                    
                    #    把导入的简历源文件与目标文件，备份到一个汇总文件夹
                    shutil.copy2(source_file_path, resume_collect_dir)
                    shutil.copy2(target_txt_file_path, resume_collect_dir)
                    
                    #    在源文件转换成目标txt文件以后，将txt文件进行导入处理
                    import_one_resume(target_txt_file_path, resume_user_dir, resume_name)
                    print("导入一条简历")
            else:
                print("源文件上传error")
        
        if not resume_file:
            print('file none')
            return HttpResponse("no files for upload!")
        else:
            return HttpResponse("upload over!")
    else:
        return render(request, 'tools_html/resume_import.html')
#         userform = UserForm(initial ={'userName': login_name})
#         return render(request, 'tools_html/resume_import.html', {'userform': userform})

       
    
#    导入一份简历
def import_one_resume(txt_file_path, resume_user_dir, resume_name):
# def import_one_resume(f):
    print("in import_one_resume")
    
#     all_text = f.read()
#     status = module_separation(all_text)
#     
#     print(status)
    
    with open(txt_file_path, "r") as f:     #    , encoding="utf-8"
#         为a+模式时，因为为追加模式，指针已经移到文尾，读出来的是一个空字符串。
#         ftext = f.read()  # 一次性读全部成一个字符串
#         ftextlist = f.readlines() # 也是一次性读全部，但每一行作为一个子句存入一个列表
         
        all_text = f.read()
        module_separation(all_text, resume_user_dir, resume_name)
        


if __name__ == '__main__':
    input_path = "F:\\ZZMK\\ZZMK_LMK_resume_files\\all_resume_txt\\"
    input_txt_name = "【产品运营】张娅飞 商业.txt"
    txt_file_path = input_path + input_txt_name
    print(txt_file_path)
    import_one_resume(txt_file_path)
    exit(0)