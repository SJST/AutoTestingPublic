from django.test import TestCase

from lmk_app.models import Candidate_resource
from bson.json_util import dumps
import re
import os
from lmk_app.lmk_tools.resume_tools.resume_name_process import get_candidate_name_from_resume_name
from lmk_app.lmk_tools.resume_tools.resume_format_process import base_symbol_format, date_format_process, module_title_format_process, module_text_format_process, special_format_process

def get_name(input_txt_name, one_module_string):
    
    name = ''
    name_from_file_name = get_candidate_name_from_resume_name(input_txt_name)
    if re.search(r"姓\s*名", one_module_string):
        name = re.search(r"姓\s*名\s*[:]*\s*([^\s]*)", one_module_string).group(1)
        
        if name != name_from_file_name:
            print(name + 'diffirent' + name_from_file_name)
            name = name_from_file_name
    
    if not name:
        name = name_from_file_name
    
    if name:
        print(name)
    
    return name

def get_telephone(one_module_string):
    telephone = ''
    if re.search(r"(联系方式|电话|手机|手机号码)\s*[:\s]\s*(\d{3}\s*-{0,1}\s*\d{4}\s*-{0,1}\s*\d{4})", one_module_string):
        telephone = re.search(r"(联系方式|电话|手机|手机号码)\s*[:\s]\s*(\d{3}\s*-{0,1}\s*\d{4}\s*-{0,1}\s*\d{4})", one_module_string).group(2)
#         print(telephone)
    elif re.search(r"(\s*\d{3}\s*-{0,1}\s*\d{4}\s*-{0,1}\s*\d{4}\s*)", one_module_string):
        telephone = re.search(r"\s*(\d{3}\s*-{0,1}\s*\d{4}\s*-{0,1}\s*\d{4})\s*", one_module_string).group(1)
#         print(telephone)
    
    if telephone:
        telephone = re.sub("-", "", telephone)
        telephone = re.sub("\s+", "", telephone)
        print(telephone)
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
        print(email)
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
    
    if education:
        print(education)
    return education

def get_other_params(all_text, update_params_dict):
    
#     education = update_params_dict['education']
    education = ''
    work_experience = ''
    temp_education = ''
    
    all_text = re.sub(r"(\d)\n", r"\1@@@\n", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub(r"@@@", "", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    
    format_flag = 0
#     if re.search(r"\n([^\n]*20\d{2}\s*[\.\-\/年]\s*\d{1,2}\s*[\-]\s*[^\n]*)", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M):
    if re.search(r"\n(^[^\n]*(20\d{2}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*[\s\-~至—]{1,2}\s*(\d{4}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*|至今))[^\n]*)", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M):
        
        format_flag = 1
        
        all_text = re.sub(r"\n(^[^\n]*(20\d{2}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*[\s\-~至—]{1,2}\s*(20\d{2}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*|至今))[^\n]*)", r"###\n\1", all_text)
#         print(all_text)
        all_module_list = list(all_text.split("###"))
#         print(all_module_list)
          
        for one_module_string in all_module_list:
#             print("\n")
              
            if re.search(r"(^[^\n]*(20\d{2}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*[\s\-~至—]{1,2}\s*(20\d{2}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*|至今))[^\n]*).*$", one_module_string, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M):
                module_obj = re.search(r"(^[^\n]*(20\d{2}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*[\s\-~至—]{1,2}\s*(20\d{2}\s*[\.\-\/年]\s*\d{1,2}\s*月{0,1}\s*|至今))[^\n]*)(.*$)", one_module_string, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
                one_module_title = module_obj.group(1)
#                     one_module_text = module_obj.group(0)
                one_module_text = module_obj.group(4)
                
                one_module_title = module_title_format_process(one_module_title)
                
                if re.search(r"(教育经历|大学院{0,1}|学院|学历|统招|本科|博士|硕士|双学位|学士(学位){0,1}|专科|大专)", one_module_title, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M):
                    temp_education += one_module_title + "\n"
                    continue
                
                one_module_text = module_text_format_process(one_module_text)
                
                one_module_text = re.sub(r"(^u|\nu)\s*", "\n", one_module_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
                
                update_params_dict = get_params_from_standard_formart(one_module_text, update_params_dict, format_flag)
                
                work_experience += one_module_title + "\n" + one_module_text + "\n"
                work_experience = re.sub(r"###.*###", "", work_experience, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
                work_experience = re.sub(r"###", "", work_experience, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
            
        if temp_education:
            update_params_dict.update({'education': temp_education})
        
        work_experience = re.sub(r"\n{1,}", "\n", work_experience, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
        
        update_params_dict.update({'work_experience': work_experience})
        
    else:
        print('not in') #    进入另一种模式，匹配原始标准的正则表达式
        update_params_dict = get_params_from_standard_formart(all_text, update_params_dict, format_flag)
        
    return update_params_dict

def get_gender(one_module_string):
    gender = ''
    if re.search(r"\s([男女])\s", one_module_string):
        gender = re.search(r"\s([男女])\s", one_module_string).group(1)
    elif re.search(r"\([^\)]*([男女])[^\)]*\)", one_module_string):
        gender = re.search(r"\([^\)]*([男女])[^\)]*\)", one_module_string).group(1)
        
    if gender:
        print(gender)
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
    
    if age:
        print(age)
    return age

def get_position_rank(one_module_string):
    position_rank = ''
    if re.search(r"(当前职位|当前职位及职级)\s*[:\s]\s*(.*)$", one_module_string):
        position_rank = re.search(r"(当前职位|当前职位及职级)\s*[:\s]\s*(.*)$", one_module_string).group(2)
#         print(position_rank)
    
    if position_rank:
        print(position_rank)
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
    
    if district_city:
        print(district_city)
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
    
    if not format_flag:
        work_experience_info_list = work_experience_info_list + ["工作经历","职业经历"]
    
    #    项目经验/项目经历
    project_experience_info_list = []     #    ["项目经历","项目经验"]  #    "主要项目经验",
    #    工作能力标签/工作能力/专业评价
    ability_info_list = ["工作能力","专业评价","工作能力标签"]
    #    语言能力
    language_info_list = ["语言能力","外语水平"]   #    ,"工作语言"
    #    证书
    certificate_info_list = ["奖励及证书","证书"]
    #    专业技能/技能标签/技能评价/IT技能
    skill_info_list = ["专业技能","技能评价","技能标签","IT技能","个人技能","熟练使用","熟练操作"]
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
        
    return update_params_dict

# def get_work_ability(one_module_string):
#     
#     return work_ability
# 
# def get_language_ability(one_module_string):
#     
#     return language_ability
# 
# def get_certificate(one_module_string):
#     
#     return certificate
# 
# def get_career_intention(one_module_string):
#     
#     return career_intention
# 
# def get_personal_profile(one_module_string):
#     
#     return personal_profile
# 
# def get_extra_info(one_module_string):
#     
#     return extra_info



#-------------------------------------------------------------------------------------------

# input_path = "F:\\ZZMK\\imported_resume\\all_collect\\"
# input_txt_name = "京东高级产品经理-何谐.txt"
# input_txt_name = "徐龙浩个人简历2018.txt"
# input_txt_name = "徐众舒_简历2018_中文.txt"
# input_txt_name = "个人简历-宗微.txt"
# txt_file_path = input_path + input_txt_name


input_path = "F:\\ZZMK\\ZZMK_LMK_resume_files\\all_resume_txt\\"
resumes_list = os.listdir(input_path)
for input_txt_name in resumes_list:
    print(input_txt_name)
#     input_txt_name = "石野 简历-New.txt"
#     input_txt_name = "简历-刘晓琳(1).txt"
#     input_txt_name = "徐龙浩个人简历2018.txt"
#     input_txt_name = "产品经理-于伟健201808.txt"
#     input_txt_name = "丁家丽-期望薪资30k-50k-工作5年以上-【脉脉招聘】.txt"
#     input_txt_name = "【产品运营】张娅飞 商业.txt"
#     input_txt_name = "孟冰简历201809.txt"
#     input_txt_name = "方雅刚--众智米奇-20181031.txt"
#     input_txt_name = "个人简历-宗微.txt"
#     input_txt_name = "中文简历-HR赵岩.txt"
#     input_txt_name = "焦振山产品经理to huawei(1).txt"
#     input_txt_name = "杨沛兵-产品.txt"
#     input_txt_name = "杨一石-北京-5年经验-高级产品经理.txt"
#     input_txt_name = "产品经理-祝攀-东北大学计算机硕士-4年.txt"
#     input_txt_name = "蒋雨池-Rachel Jiang.txt"
    
    filter_params_dict = {}
    update_params_dict = {}
    
    txt_file_path = input_path + input_txt_name
    with open(txt_file_path, "r") as f:
        all_text = f.read()
        
        all_text = special_format_process(all_text)
        
        all_text = base_symbol_format(all_text)
        
        all_text = re.sub(r"(\d)\s*\)", r"\1)", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
        
        all_text = date_format_process(all_text)
        
        all_text = re.sub(r"·{1,}", r"\t", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
        
#         all_text = re.sub(r"(20\d{2})\s*年\s*(\d{1,2})\s*月", r"\1年\2月 ", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
        
        all_text = re.sub(r"项目经验\s*", r"项目经验 \n", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
        
        print("---------------------")
        name = get_name(input_txt_name, all_text)
        telephone = get_telephone(all_text)
        email = get_email(all_text)
        education = get_education(all_text)
        print("---------------------")
        gender = get_gender(all_text)
        age = get_age(all_text)
        position_rank = get_position_rank(all_text)
        district_city = get_district_city(all_text)
        print("---------------------")
        
        filter_params_dict.update({'telephone': telephone})
        update_params_dict.update({'name': name, 'gender': gender, 'age': age, 'email': email, 'position': position_rank, 'education': education})
        
        update_params_dict = get_other_params(all_text, update_params_dict)
        
        work_experience = ''
        if 'work_experience' in update_params_dict:
            work_experience = update_params_dict['work_experience']
        
        for key in update_params_dict:
            
            if key != 'work_experience':
                work_experience = work_experience.replace(update_params_dict[key], "", re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
                print(key + "\n")
                print(update_params_dict[key] + "\n")
            
        print(work_experience)
        update_params_dict.update({'work_experience': work_experience})
        
        if not name:
            print("name error")
#             return
         
        if not telephone:
            print("telephone error")
#             return
         
        if not email:
            print("email error")
#             return
 
        if not education:
            print("education error")
#             return
        
        print("---------------------")
#         print("done---------------------")





