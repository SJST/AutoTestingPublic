
# coding=utf-8

from win32com import client as wc
import os
import re
import time

def doc_to_docx(resume_file_path, new_resume_file_path):
    word = wc.Dispatch("Word.Application")
    
    doc = word.Documents.Open(resume_file_path)
    doc.SaveAs(new_resume_file_path, 16)    #   12为docx
    doc.Close()
    word.Quit()
    
    
if __name__ == '__main__':
    resume_dir_path = "D:\\ZZMK_LMK_resume_files\\all_resume\\doc\\"
    new_resume_dir_path = "D:\\ZZMK_LMK_resume_files\\all_resume\\docx\\"
    
    resumes_list = os.listdir(resume_dir_path)
    
    start_time = time.time()
    print('begin doc_to_docx')
    
    for doc_name in resumes_list:
        file_name = re.match('([^\.]*)\.doc$', doc_name).group(1)
        
        resume_file_path = resume_dir_path + "\\" + doc_name
        new_resume_file_path = new_resume_dir_path + "\\" + file_name + ".docx"
        
        # 如果写入文件存在，则清空文件或者删除文件
        if(not os.path.exists(new_resume_file_path)):
            doc_to_docx(resume_file_path, new_resume_file_path)
        else:
#             print('resume_file_path: ' + resume_file_path)
            print(new_resume_file_path)
            print('exist')
    
    print('end doc_to_docx')
    end_time = time.time()
    print('总共耗时：' + str(end_time - start_time) + 's')
    