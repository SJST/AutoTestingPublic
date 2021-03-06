'''
Created on 2018-11-8

@author: P0044185
'''

# coding=utf-8
import re
import sys
from lmk_app.lmk_tools.record_logs_tools.process_logs import bad_code_collection_write, bad_code_clean
from lmk_app.lmk_tools.record_logs_tools.process_logs import bad_code_collection_read

#    删除字母之间的空格
def space_process(results):
    
    results = remove_chinese_character_space(results)
    results = remove_number_space(results)
    results = remove_character_space(results)
    results = remove_number_point_space(results)
    
    return results

#    处理异常，递归函数
def recursive_process_UnicodeEncodeError(f, results):
    
    #---    for bad coding exception
    try:
        f.write(results + '\n')
    except UnicodeEncodeError:
        #    for result has more badcode
        print('UnicodeEncodeError:', sys.exc_info()[1])
        
        error_info_string = str(sys.exc_info()[1])
        
        if(re.search(r"character '[^']*'", error_info_string)):
            bad_code = re.search(r"character '([^']*)'", error_info_string).group(1)
            print(bad_code)
            bad_code_collection_write(bad_code)
            
            all_lines_string = bad_code_collection_read()
            results = bad_code_clean(all_lines_string, results)
            
        recursive_process_UnicodeEncodeError(f, results)
#     finally:
#         print(results)
    
    return results

#    删除数字小数点之间的空格
def remove_number_point_space(results):
    results = results
    
    while(re.search('((\d)\s(\.)\s(\d))', results, re.RegexFlag.S|re.RegexFlag.M)):
        re_result = re.search('((\d)\s(\.)\s(\d))', results, re.RegexFlag.S|re.RegexFlag.M)
        
        old_string = re_result.group(1)
        new_string = re_result.group(2) + re_result.group(3) + re_result.group(4)
        
        results = re.sub(old_string, new_string, results, re.RegexFlag.S|re.RegexFlag.M)
        
#     results = re.sub('^\s+|\s+$', '', results)
    
    return results

#    删除汉字之间的空格
def remove_chinese_character_space(results):
#     results = results
#     
#     while(re.search('(([\u4E00-\u9FA5]) ([\u4E00-\u9FA5]))', results, re.RegexFlag.S)):    #    |re.RegexFlag.M
#         re_result = re.search('(([\u4E00-\u9FA5]) ([\u4E00-\u9FA5]))', results, re.RegexFlag.S)    #    |re.RegexFlag.M
#         
#         old_string = re_result.group(1)
#         new_string = re_result.group(2) + re_result.group(3)
#         
#         results = re.sub(old_string, new_string, results, re.RegexFlag.S|re.RegexFlag.M)
#         
#     results = re.sub('^\s+|\s+$', '', results)
    
    return results

#    删除数字之间的空格
def remove_number_space(results):
    results = results
    
    while(re.search('((\d)\s([\d]))', results, re.RegexFlag.S|re.RegexFlag.M)):
        re_result = re.search('((\d)\s([\d]))', results, re.RegexFlag.S|re.RegexFlag.M)
        
        old_string = re_result.group(1)
        new_string = re_result.group(2) + re_result.group(3)
        
        results = re.sub(old_string, new_string, results, re.RegexFlag.S|re.RegexFlag.M)
        
#     results = re.sub('\s+', ' ', results)
#     results = re.sub('^\s+|\s+$', '', results)
#     print(results)
    
    return results

#    删除字母之间的空格
def remove_character_space(results):
    results = results
    
    while(re.search('(([a-zA-z])\s([a-zA-z]))', results, re.RegexFlag.S|re.RegexFlag.M)):
        re_result = re.search('(([a-zA-z])\s([a-zA-z]))', results, re.RegexFlag.S|re.RegexFlag.M)
        
        old_string = re_result.group(1)
        new_string = re_result.group(2) + re_result.group(3)
        
        results = re.sub(old_string, new_string, results, re.RegexFlag.S|re.RegexFlag.M)
        
#     results = re.sub('\s+', ' ', results)
#     results = re.sub('^\s+|\s+$', '', results)
#     print(results)
    
    return results

    