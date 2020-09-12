
# coding=utf-8
import os
import sys
import importlib
importlib.reload(sys)
import time
import re

from lmk_app.lmk_tools.resume_tools.read_file_pdf import read_pdf
from lmk_app.lmk_tools.resume_tools.read_file_word import read_word

if __name__ == '__main__':
    start_time = time.time()
    
    resume_dir_path = 'D:\ZZMK_LMK_resume_files\\all_resume'
    resume_txt_dir_path = 'D:\ZZMK_LMK_resume_files\\all_resume_txt'
     
    resumes_list = os.listdir(resume_dir_path)
    
    pdf_count = 0
    docx_count = 0
    other_count = 0
    for dir_name in resumes_list:
        print(dir_name)
        
        if(re.match('^doc$', dir_name)):
            continue
        
#         if(re.match('^docx$', dir_name)):
#             continue
        
        resume_sub_dir_path = resume_dir_path + "\\" + dir_name
        
        if(os.path.isdir(resume_sub_dir_path)):
            
            resumes_sub_list = os.listdir(resume_sub_dir_path)
            
            for file_name in resumes_sub_list:
                
                if(re.search('([^\.]*)\.', file_name)):
                    resume_name = re.match('([^\.]*)\.', file_name).group(1)
                else:
                    resume_name = file_name
                
                print("\n")
                print(resume_name)
                
                if(re.search('\.docx$', file_name)):
                    resume_file_path = resume_sub_dir_path + "\\" + file_name
                    txt_output_path = resume_txt_dir_path + "\\" + resume_name + ".txt"
                    
                    print(resume_file_path)
                    print(txt_output_path)
                    
                    read_word(resume_file_path, txt_output_path)
                    docx_count += 1
                elif(re.search('\.pdf$', file_name)):
                    resume_file_path = resume_sub_dir_path + "\\" + file_name
                    txt_output_path = resume_txt_dir_path + "\\" + resume_name + ".txt"
                     
                    print(resume_file_path)
                    print(txt_output_path)
                     
                    read_pdf(resume_file_path, txt_output_path)
                    pdf_count += 1
                else:
                    other_count += 1
    
    print(docx_count)
    print(pdf_count)
    print(other_count)
        
    exit(0)
    
    resume_file_path = "D:\ZZMK_LMK_resume_files\丁家丽-期望薪资30k-50k-工作5年以上-【脉脉招聘】.pdf"
    txt_output_path = "D:\ZZMK_LMK_resume_files\丁家丽-期望薪资30k-50k-工作5年以上-【脉脉招聘】.txt"
     
    read_pdf(resume_file_path, txt_output_path)
    
    resume_file_path = "D:\ZZMK_LMK_resume_files\方雅刚--众智米奇-20181031.docx"
    txt_output_path = "D:\ZZMK_LMK_resume_files\方雅刚--众智米奇-20181031.txt"
    
    read_word(resume_file_path, txt_output_path)
    
    end_time = time.time()
    print('ok,解析pdf结束!')
    print('总共耗时：' + str(end_time - start_time) + 's')
    
