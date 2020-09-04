import re
import os

def base_symbol_format(all_text):
    all_text = re.sub("“", "\"", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub("”", "\"", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    
    all_text = re.sub("：", ": ", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub("，", ",", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub("～", "~", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub("~", "-", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub("—", "-", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub("（", "(", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub("）", ")", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub("；", ";", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub("︳", " ", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub("\|", " ", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub(r"(\d{4}\.(\d{4}))", "\1 - \2", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub(r"(^[a-zA-Z]|\n[a-zA-Z])\s*", "\n", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    
    return all_text

def date_format_process(all_text):
    all_text = re.sub(r"(20\d{2})\s*[\-\.\/—~年]\s*(\d{1,2})(\s*月){0,1}\s*(\d{1,2})\s*日", r"\1.\2.\4", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub(r"(20\d{2})\s*[\-\.\/—~年]\s*(\d{1,2})(\s*月){0,1}", r"\1.\2", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub(r"(\d{4})\.(\d[^\d])", r"\1.0\2", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub(r"([\d])\s*([\-——~至到])\s*(\d)", r"\1 \2 \3", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub(r"(\d)\s*([\-——~至])\s*(至{0,1}今)", r"\1 \2 \3", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    
    return all_text

def module_title_format_process(module_title):
    module_title = re.sub(r"--", "-", module_title, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    module_title = re.sub(r"\s至\s", r" - ", module_title, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    
    module_title = base_symbol_format(module_title)
    module_title = date_format_process(module_title)
    
    module_title = re.sub(r"([^\(^\s^、])(20\d{2}\.)", r"\1\t\2", module_title, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    module_title = re.sub(r"(\.\d{2})([^\s^\)])", r"\1\t\2", module_title, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    module_title = re.sub(r"(至今)([^\s^\)])", r"\1\t\2", module_title, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    
    module_title = re.sub(r"@@@", "", module_title, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    module_title = re.sub(r"\s{2,}", r"\t", module_title, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    module_title = re.sub(r"^\s+|\s+$", "", module_title, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    
    return module_title

def module_text_format_process(module_text):
    module_text = re.sub(r"--", "-", module_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    module_text = re.sub(r"\s至\s", r" - ", module_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    
    module_text = base_symbol_format(module_text)
    module_text = date_format_process(module_text)
    
    module_text = re.sub(r"([^\(^\s^、])(20\d{2}\.)", r"\1\t\2", module_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    module_text = re.sub(r"(\.\d{2})([^\s^\)])", r"\1\t\2", module_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    module_text = re.sub(r"(\d\.)\s*", r"\1", module_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    module_text = re.sub(r"(至今)([^\s^\)])", r"\1\t\2", module_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    
#     module_text = re.sub(r"项目经验\s*[:]{0,1}", "", module_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    module_text = re.sub(r"教育背景\s*[:]{0,1}", "", module_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    
    module_text = re.sub(r"@@@", "", module_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    module_text = re.sub(r"###.*###", "", module_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    module_text = re.sub(r"###", "", module_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    module_text = re.sub(r"^\s+|\s+$", "", module_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    
    return module_text

def special_format_process(all_text):
    all_text = re.sub(r"--", "-", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    all_text = re.sub(r"\.-\s*", "-", all_text, re.RegexFlag.I|re.RegexFlag.S|re.RegexFlag.M)
    return all_text



