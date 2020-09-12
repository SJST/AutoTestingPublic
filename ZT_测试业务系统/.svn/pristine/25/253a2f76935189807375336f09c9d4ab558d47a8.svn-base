
import re
import json
import time
from datetime import date
from bson.json_util import dumps

from lmk_app.models import Candidate_user
from lmk_app.models import Candidate_resource
from lmk_app.models import One_remark, One_prompt

from django.shortcuts import render, redirect, HttpResponse
from test.test_long import special

#    模块分离
def module_separation(all_text):
    #    个人信息/个人资料/基本信息/基本资料
    personal_base_info_list = ["个人信息","个人资料","基本信息","基本资料"]
    #    个人简介
    profile_info_list = ["个人简介"]
    #    教育背景/教育经历
    education_info_list = ["教育背景","教育经历"]
    #    工作经历/工作经验
    work_experience_info_list = ["工作经历","工作经验"]
    #    项目经验/项目经历
    project_experience_info_list = ["项目经历","项目经验"]
    #    工作能力标签/工作能力/专业评价
    ability_info_list = ["工作能力","专业评价","工作能力标签"]
    #    语言能力
    language_info_list = ["语言能力"]
    #    证书
    certificate_info_list = ["证书"]
    #    专业技能/技能标签/技能评价/IT技能
    skill_info_list = ["专业技能","技能评价","技能标签","IT技能"]
    #    求职信息/求职意向/职业意向
    intention_info_list = ["求职信息","求职意向","职业意向"]
    #    自我评价
    self_evaluation_info_list = ["自我评价"]
    #    附加信息
    extra_info_list = ["附加信息"]
    #    兴趣爱好
    hobby_info_list = ["兴趣爱好"]
    
    all_module_title_info_list = [personal_base_info_list, profile_info_list, education_info_list, 
                     work_experience_info_list, project_experience_info_list, ability_info_list, 
                     language_info_list, certificate_info_list, skill_info_list, intention_info_list, 
                     self_evaluation_info_list, extra_info_list, hobby_info_list]
    all_module_title_info_string = str(all_module_title_info_list)
    
    all_text = re.sub("：", ":", all_text)
    all_text = re.sub("，", ",", all_text)
    all_text = re.sub("～", "~", all_text)
    all_text = re.sub("（", "(", all_text)
    all_text = re.sub("）", ")", all_text)
    all_text = re.sub("；", ";", all_text)
    
    all_text = re.sub("项目经验\s*", "项目经验 ", all_text)
    
    all_text = '###' + all_text
    for one_info_list in all_module_title_info_list:
        for one_string in one_info_list:
            if re.search(one_string, all_text):
                all_text = re.sub(one_string, "###" + one_string, all_text)
#                 print(all_text)
                continue
    
#     print(all_text)
    
    module_list = all_text.split("###")
    
    name = ''
    telephone = ''
    email = ''
    age = ''
    education = ''
    
    special_module_dict = {}
    normal_module_dict = {}
    for one_module_string in module_list:
        if re.search(r"^([^:\s]*)[:\s]\s*(.*)$", one_module_string, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M):
            module_obj = re.search(r"^([^:\s]*)[:\s]\s*(.*)$", one_module_string, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
            one_module_title = module_obj.group(1)
            one_module_text = module_obj.group(2)
            
            if one_module_title not in all_module_title_info_string:
                special_module_dict[one_module_title] = one_module_text
            else:
                normal_module_dict[one_module_title] = one_module_text
                
            print(one_module_title + ":\n" + one_module_text)
        else:
            continue
        
        if re.search(r"姓名", one_module_string):
            name = re.search(r"姓名\s*[:]*\s+([^\s]*)", one_module_string).group(1)
            print(name)
            
        if re.search(r"(联系方式|电话)\s*[:\s]\s*([^\s]*)", one_module_string):
            telephone = re.search(r"(联系方式|电话)\s*[:\s]\s*([^\s]*)", one_module_string).group(2)
            print(telephone)
        
        if re.search(r"邮箱|email", one_module_string):
            email = re.search(r"(邮箱|email)\s*[:]*\s+([^\s]*)", one_module_string).group(2)
            print(email)
        
        if re.search(r"出生", one_module_string):
            age = re.search(r"(出生日期|出生年月|生日|年龄)\s*[:]*\s+([^\s]*)", one_module_string).group(2)
            print(age)
        
        if re.search(r"学历|统招|本科|博士|硕士|双学位|学士学位|专科|大专", one_module_string):
            if re.search(r"学历\s*[:]*\s+([^\s]*)", one_module_string):
                education  = re.search(r"学历\s*[:]*\s+([^\s]*)", one_module_string).group(1)
            else:
                education  = re.search(r"([^\s^\(\)]*(统招|本科|博士|硕士|双学位|学士学位|专科|大专)[^\s^\(^\)]*)", one_module_string).group(1)
            
            print(education)
        
    if special_module_dict:
        for module_title in special_module_dict:
            name = re.sub(r"(籍贯|民族|政治).*$", "", module_title)
            
            module_text = special_module_dict[module_title]
            if re.search(r"(^\d+岁)", module_text):
                age = re.search(r"(\d+岁)", module_text).group(1)
                print(age)
            
#             if re.search(r"(\s*([^\s]*市[^\s]*)\s*)", module_text):
#                 district_city = re.search(r"(\s*([^\s]*市[^\s]*)\s*)", module_text).group(1)
#                 print(district_city)
            
            if re.search(r"(\s*\d{11}\s*)", module_text):
                telephone = re.search(r"\s*(\d{11})\s*", module_text).group(1)
                print(telephone)
            
            if re.search(r"\s*([^\s]*\@[^\s]*)\s*", module_text):
                email = re.search(r"\s*([^\s]*\@[^\s]*)\s*", module_text).group(1)
                print(email)
        
    if not name:
        print("name error")
        return
    
    if not telephone:
        print("telephone error")
        return
    
    if not email:
        print("email error")
        return
    
    if not age:
        print("age error")
        return
    
    if not education:
        print("education error")
        return
    
    filter_params_dict = {}
    update_params_dict = {}
    
    filter_params_dict.update({'telephone': telephone})
    
    update_params_dict.update({'name': name, 'email': email, 'age': age, 'education': education})
    
    for module_title in normal_module_dict:
        module_text = normal_module_dict[module_title]
        
        module_text = re.sub("^\s*ABOUT\s*ME\s*", "", module_text)
        module_text = re.sub("^\s*EDUCATION\s*", "", module_text)
        module_text = re.sub("^\s*WORKEXPERIENCE\s*", "", module_text)
        module_text = re.sub("^\s*PROJECTEXPERIENCE\s*", "", module_text)
        module_text = re.sub("^\s*SKILL\s*", "", module_text)
        
        module_text = re.sub(r"(20\d{2}[.-]\d{1,2}\s*-)", r"\n\1", module_text)
        module_text = re.sub("^\s+", "", module_text)
        
        if module_title in education_info_list:
            update_params_dict.update({'education': module_text})
        elif module_title in work_experience_info_list:
            update_params_dict.update({'work_experience': module_text})
        elif module_title in project_experience_info_list:
            update_params_dict.update({'project_experience': module_text})
        elif module_title in skill_info_list:
            update_params_dict.update({'skills': module_text})
        
        elif module_title in profile_info_list:
            update_params_dict.update({'personal_profile': module_text})
        elif module_title in ability_info_list:
            update_params_dict.update({'work_ability': module_text})
        elif module_title in language_info_list:
            update_params_dict.update({'language_ability': module_text})
        elif module_title in certificate_info_list:
            update_params_dict.update({'certificate': module_text})
        elif module_title in intention_info_list:
            update_params_dict.update({'career_intention': module_text})
        elif module_title in self_evaluation_info_list:
            update_params_dict.update({'self_evaluation': module_text})
        elif module_title in extra_info_list:
            update_params_dict.update({'extra_info': module_text})
        elif module_title in hobby_info_list:
            update_params_dict.update({'hobby_info': module_text})
        
    candidate_obj = Candidate_resource.objects(**filter_params_dict).update(upsert= True, **update_params_dict)
    if candidate_obj:
        status = 'success'    
        
    
    
    
    
#    导入一份简历
# def import_one_resume(txt_file_path):
def import_one_resume(f):
    print("in import_one_resume")
    
    all_text = f.read()
    module_separation(all_text)
    
#     with open(txt_file_path, "r") as f:     #    , encoding="utf-8"
# #         为a+模式时，因为为追加模式，指针已经移到文尾，读出来的是一个空字符串。
# #         ftext = f.read()  # 一次性读全部成一个字符串
# #         ftextlist = f.readlines() # 也是一次性读全部，但每一行作为一个子句存入一个列表
#         
#         all_text = f.read()
#         module_separation(all_text)
        


if __name__ == '__main__':
    input_path = "F:\\ZZMK\\ZZMK_LMK_resume_files\\all_resume_txt\\"
    input_txt_name = "【产品运营】张娅飞 商业.txt"
    txt_file_path = input_path + input_txt_name
    print(txt_file_path)
    import_one_resume(txt_file_path)
    exit(0)