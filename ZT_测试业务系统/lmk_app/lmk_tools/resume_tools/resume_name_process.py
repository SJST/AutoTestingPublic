import re
import os

def get_candidate_name_from_resume_name(resume_name):
    
    original_resume_name = resume_name
    resume_name = re.sub(r'[【】（）]', ' ', resume_name, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    resume_name = re.sub(r"(简历)", "", resume_name, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    resume_name = re.sub(r"(产品|经理|运营|应聘|高级|商业|风控|前端)", "", resume_name, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    resume_name = re.sub(r"(中文|英文|日文|韩文)", "", resume_name, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    resume_name = re.sub(r"(北京|上海|深圳|杭州|广州|大连)", "", resume_name, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    resume_name = re.sub(r"(\d\s*年)", "", resume_name, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    resume_name = re.sub(r"\([^\)]\)", "", resume_name, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    resume_name = re.sub(r"[a-zA-Z0-9]", "", resume_name, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    resume_name = re.sub(r"\s+", "", resume_name, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    resume_name = re.sub(r"^[-_]{1,}|[-_]{1,}$", "", resume_name, re.RegexFlag.I|re.RegexFlag.S)
    resume_name = re.sub(r"^\.$", "", resume_name, re.RegexFlag.I|re.RegexFlag.S)
    # name = re.search(r"[-{1,2}]([\u4E00-\u9FA5]{2,4})\.[^\.]*$", resume_name).group(1)
    
    name = ''
    if re.search(r"-", resume_name):
        if re.search(r"[-{1,2}]([\u4E00-\u9FA5]{2,3})\.[^\.]*$", resume_name):
            name = re.search(r"[-{1,2}]([\u4E00-\u9FA5]{2,3})\.[^\.]*$", resume_name).group(1)
        elif re.search(r"^([\u4E00-\u9FA5]{2,3})[-{1,2}]", resume_name):
            name = re.search(r"^([\u4E00-\u9FA5]{2,3})[-{1,2}]", resume_name).group(1)
        else:
            name = name_no_symbol(resume_name)
    
    elif re.search(r"_", resume_name):
        if re.search(r"[_{1,2}]([\u4E00-\u9FA5]{2,3})\.[^\.]*$", resume_name):
            name = re.search(r"[_{1,2}]([\u4E00-\u9FA5]{2,3})\.[^\.]*$", resume_name).group(1)
        elif re.search(r"^([\u4E00-\u9FA5]{2,3})[_{1,2}]", resume_name):
            name = re.search(r"^([\u4E00-\u9FA5]{2,3})[_{1,2}]", resume_name).group(1)
        else:
            name = name_no_symbol(resume_name)
    
    else:
        name = name_no_symbol(resume_name)
    
    if not name:
        return ''
    else:
        return name

def name_no_symbol(resume_name):
    name = ''
    if re.search(r"^([\u4E00-\u9FA5]{2,3})的个人简历", resume_name):
        name = re.search(r"^([\u4E00-\u9FA5]{2,3})的个人简历", resume_name).group(1)
#         print(name)
    
    elif re.search(r"^([\u4E00-\u9FA5]{2,3})个人简历", resume_name):
        name = re.search(r"^([\u4E00-\u9FA5]{2,3})个人简历", resume_name).group(1)
#         print(name)
    
    elif re.search(r"^([\u4E00-\u9FA5]{2,3})的简历", resume_name):
        name = re.search(r"^([\u4E00-\u9FA5]{2,3})的简历", resume_name).group(1)
#         print(name)
           
    elif re.search(r"^([\u4E00-\u9FA5]{2,3})简历", resume_name):
        name = re.search(r"^([\u4E00-\u9FA5]{2,3})简历", resume_name).group(1)
#         print(name)
    elif re.search(r"^([\u4E00-\u9FA5]{2,3})\.", resume_name):
        name = re.search(r"^([\u4E00-\u9FA5]{2,3})\.", resume_name).group(1)
#         print(name)
        
    if name:
        return name
    else:
        return resume_name

# resume_dir_path = "F:\\ZZMK\\ZZMK_LMK_resume_files\\all_resume_txt"
# resumes_list = os.listdir(resume_dir_path)
# 
# for resume_name in resumes_list:
# 
#     print(resume_name)
#     original_resume_name = resume_name
#     
#     resume_name = re.sub(r'[【】（）]', ' ', resume_name, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
#     resume_name = re.sub(r"(产品|经理|运营|应聘|高级|商业|风控)", "", resume_name, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
#     resume_name = re.sub(r"(北京|上海|深圳|杭州|广州|大连)", "", resume_name, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
#     resume_name = re.sub(r"\([^\)]\)", "", resume_name, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
#     resume_name = re.sub(r"[a-zA-Z0-9]", "", resume_name, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
#     resume_name = re.sub(r"\s+", "", resume_name, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
#     resume_name = re.sub(r"^-{1,}|-{1,}$", "", resume_name, re.RegexFlag.I|re.RegexFlag.S)
#     resume_name = re.sub(r"^\.$", "", resume_name, re.RegexFlag.I|re.RegexFlag.S)
#     # name = re.search(r"[-{1,2}]([\u4E00-\u9FA5]{2,4})\.[^\.]*$", resume_name).group(1)
#     
#     name = ''
#     if re.search(r"-", resume_name):
#         if re.search(r"[-{1,2}]([\u4E00-\u9FA5]{2,3})\.[^\.]*$", resume_name):
#             name = re.search(r"[-{1,2}]([\u4E00-\u9FA5]{2,3})\.[^\.]*$", resume_name).group(1)
#         elif re.search(r"^([\u4E00-\u9FA5]{2,3})[-{1,2}]", resume_name):
#             name = re.search(r"^([\u4E00-\u9FA5]{2,3})[-{1,2}]", resume_name).group(1)
#         else:
#             name = name_no_symbol(resume_name)
#     
#     elif re.search(r"_", resume_name):
#         if re.search(r"[_{1,2}]([\u4E00-\u9FA5]{2,3})\.[^\.]*$", resume_name):
#             name = re.search(r"[_{1,2}]([\u4E00-\u9FA5]{2,3})\.[^\.]*$", resume_name).group(1)
#         elif re.search(r"^([\u4E00-\u9FA5]{2,3})[_{1,2}]", resume_name):
#             name = re.search(r"^([\u4E00-\u9FA5]{2,3})[_{1,2}]", resume_name).group(1)
#         else:
#             name = name_no_symbol(resume_name)
#     
#     else:
#         name = name_no_symbol(resume_name)
#     
#     if not name:
#         print('no name')
#     else:
#         print(name)
