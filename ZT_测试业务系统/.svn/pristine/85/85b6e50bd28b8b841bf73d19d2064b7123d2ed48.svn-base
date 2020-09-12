
# coding=utf-8
import os
import sys
import importlib
importlib.reload(sys)

from lmk_app.lmk_tools.resume_tools.string_process import space_process
from lmk_app.lmk_tools.resume_tools.string_process import recursive_process_UnicodeEncodeError
from lmk_app.lmk_tools.record_logs_tools.process_logs import bad_code_collection_read
from lmk_app.lmk_tools.record_logs_tools.process_logs import bad_code_clean

#读取docx中的文本代码示例
import docx

'''
 解析word 文本，保存到txt文件中
'''

def read_word(resume_file_path, txt_output_path):
    #获取文档对象
    resume_file = docx.Document(resume_file_path)
    print("段落数:"+str(len(resume_file.paragraphs)))
    
    # 如果写入文件存在，则清空文件或者删除文件
    if(os.path.exists(txt_output_path)):
        os.remove(txt_output_path)
        print('exist and remove')
        
    #输出每一段的内容
    for para in resume_file.paragraphs:
#         print(para.text)
        
        with open(txt_output_path, 'a') as f:  #    , encoding='utf-8'
            results = para.text
            
            all_lines_string = bad_code_collection_read()
            results = bad_code_clean(all_lines_string, results)
            
            results = space_process(results)
            
            results = recursive_process_UnicodeEncodeError(f, results)
            
            print(results)
    
#     #输出段落编号及段落内容
#     for i in range(len(resume_file.paragraphs)):
#         print("第"+str(i)+"段的内容是："+resume_file.paragraphs[i].text)
    
if __name__ == '__main__':
    resume_file_path = "F:\\ZZMK\\ZZMK_LMK_resume_files\\all_resume\\docx\\方雅刚--众智米奇-20181031.docx"
    txt_output_path = "D:\ZZMK_LMK_resume_files\方雅刚--众智米奇-20181031.txt"
    
    read_word(resume_file_path, txt_output_path)
    
