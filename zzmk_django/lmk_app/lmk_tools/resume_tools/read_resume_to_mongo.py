
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
     
    resumes_list = os.listdir(resume_dir_path)
    
    for dir_name in resumes_list:
        print(dir_name)
    exit(0)
    
    pdf_count = 0
    doc_count = 0
    docx_count = 0
    for file_name in resumes_list:
        print(file_name)
        if(re.search('\.pdf$', file_name)):
            pdf_count += 1
        elif(re.search('\.docx$', file_name)):
            docx_count += 1
     
    print(pdf_count)
    print(doc_count)
    print(docx_count)
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
    
