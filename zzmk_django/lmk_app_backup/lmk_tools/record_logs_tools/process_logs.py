'''
Created on 2018-11-8

@author: P0044185
'''

import re

zzmk_django_logs_dir_path = 'E:\\workspace\\zzmk_django_logs'

resume_file_logs_dir_path = zzmk_django_logs_dir_path + "\\resume_file_logs\\"

bad_code_file_name = "bad_code_collection.txt"
read_failed_log_name = "read_failed_files_log.txt"

bad_code_file_path = resume_file_logs_dir_path + bad_code_file_name
read_failed_log_path = resume_file_logs_dir_path + read_failed_log_name

def read_failed_logs(resume_file_path):
    
    print(resume_file_path)
    with open(read_failed_log_path, mode='a+', encoding='utf-8') as f:
        f.write(resume_file_path + ',\n')

        


#---    乱码收集，如果检测到乱码异常，将乱码存入txt中，
#---    当简历文件解析下一页之前，将txt中的乱码遍历替换掉，如果检测到新乱码，重复操作
def bad_code_collection_write(bad_code):
    
    print(bad_code_file_path)
    
    with open(bad_code_file_path, mode='r+', encoding='utf-8') as f:  #    , encoding='utf-8'
        lines_array = f.readlines()
        
        if(len(lines_array) == 0):
            f.write(bad_code)
        
        for line in lines_array:
            if(line == ''):
                f.write(bad_code)
            elif(re.search(r"\n$", line)):
                continue
            else:
                if(len(re.findall(',', line)) < 19):
                    f.write(',' + bad_code)
                elif(len(re.findall(',', line)) == 19):
                    f.write(',\n' + bad_code)

def bad_code_collection_read():
    
    with open(bad_code_file_path, 'r', encoding='utf-8') as f:  #    , encoding='utf-8'
        all_lines_string = f.read()
        
    return all_lines_string
        
def bad_code_clean(all_lines_string, results):
    if(all_lines_string == ''):
        return results
    
    all_bad_code_array = re.split(',', all_lines_string, flags=re.RegexFlag.M)
    
    for bad_code in all_bad_code_array:
#         results = re.sub(r"\%s" %bad_code, "", results)
        results = re.sub(bad_code, "", results)
        
    return results


if __name__ == '__main__':
#     read_failed_logs()
    bad_code = '\\u0026'
#     bad_code_collection_write(bad_code)
    bad_code_collection_read(bad_code)
    exit(0)
    
    for num in range(30):
        bad_code_collection_write(bad_code)
        
        if(num == 30):
            print(30)
