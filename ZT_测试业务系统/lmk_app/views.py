
# from lmk_app.models import Candidate_resource
import os
import string,random
import sys
import importlib
from lmk_app.Cs01_CommonMethod import StrMehod
importlib.reload(sys)

from lmk_app.Contants import DataBaseFeildContants,SystemContants
from lmk_app.models import Candidate_user, SingleValue, SwaggerCommon
from lmk_app.models import Candidate_resource
from lmk_app.models import One_remark, One_prompt
from lmk_app.models import Skin_color
from lmk_app.models import Role, Permission
from lmk_app.models import new_company,position_classification,position_info

import time
from datetime import date

import re
from bson.json_util import dumps
import json
from django.template.context_processors import request
# from pip._vendor.urllib3.poolmanager import key_fn_by_scheme

try:
    from django.http import JsonResponse
except ImportError:
    from lmk_app_backup import JsonResponse

from pymongo import MongoClient
import pymongo

from functools import wraps
from django.shortcuts import render, render_to_response, redirect, HttpResponse

#    根据dict的key排序list中的dict    排序包
from operator import itemgetter

#    新用户注册，注册之后等待管理员审批授权
def register_info(request):
    if request.method == "POST":
        update_params_dict = {}
    
        for key, value in request.POST.items():
            if key == 'telephone':
                value = int(value)
                update_params_dict.update({key: value})
            elif re.search(r'time$', key) or re.search(r'day$', key) or re.search(r'date$', key):
                if value:
                    if isinstance(value, str):
                        #    用time模块    print (timeArray.tm_year)    #2018
                        #    print (timeArray )    #time.struct_time(tm_year=2018, tm_mon=12, tm_mday=3, tm_hour=20, tm_min=40, tm_sec=0, tm_wday=0, tm_yday=337, tm_isdst=-1)
                        time_array = time.strptime(value, "%Y-%m-%d")
                        time_strp = int(time.mktime(time_array))
                        time_iso_obj = date.fromtimestamp(time_strp)
                        
#                         #    用datetime模块    print (datetimeArray.year) #2018
#                         datetimeArray=datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
#                         timeStamp1=time.mktime(datetimeArray.timetuple())
                        print(key)
                        print(value)
                        print(time_array)
                        print(time_strp)
                        
                        #    需要把时间戳转换成date对象，才能存入mongodb中
                        update_params_dict.update({key: time_iso_obj})
            else:
                if value:
                    update_params_dict.update({key: value})
                    
        if update_params_dict:
            candidate_obj = Candidate_user(**update_params_dict)
            candidate_obj.save()
            
            #    时间戳
            date_strf = time.time()
            #    格式化时间
            format_time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            one_prompt = One_prompt(login_name=update_params_dict['login_name'], register_real_name=update_params_dict['real_name'], date_strf=date_strf, date_string=format_time_string)
            
            admin_prompt_update_obj = Candidate_user.objects(role_name__endswith="管理员").update(upsert= True, push__prompt_message=one_prompt)
#             super_prompt_update_obj = Candidate_user.objects(real_name="王为冬").update(upsert= True, push__prompt_message=one_prompt)
            
            if admin_prompt_update_obj:
                print("success add a prompt message")
            else:
                print("failed add a prompt message")
            
            status = 'success'
            return HttpResponse(status)
        
    return render(request, 'register.html')

# 说明：这个装饰器的作用，就是在每个视图函数被调用时，都验证下有没法有登录，
# 如果有过登录，则可以执行新的视图函数，
# 否则没有登录则自动跳转到登录页面。
def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
#         if re.match(r'\/$', request.path):
#             print("500")
#             return redirect('login')
         
        if request.session.get('is_login')=='1':
            return f(request,*arg,**kwargs)
        else:
            return redirect('login')
    return inner

#    用户登陆之后的界面，根据用户角色决定页面功能的显示
@check_login
def index(request):
    # return render(request, 'test_index.html')

#     user_id = request.session.get('user_id')
    login_name = request.session.get('login_name')
#     user_id = '5bd038a76c92a52074dc29e3'

    # 使用user_id去数据库中找到对应的user信息
#     userobj = Candidate_user.objects.filter(_id=user_id)

    if login_name:
#         userobj = Candidate_user.objects.filter(login_name=login_name)
        userobj = Candidate_user.objects.filter(login_name=login_name).as_pymongo()
    else:
        return redirect('login')
    
    skin_color_obj = Skin_color.objects.order_by("color_code")
    
    skin_color_dict = {}
    
    for one_color in skin_color_obj:
        if one_color:
            skin_color_dict.update({one_color.color_code: one_color.color_name})

#     #---
#     userobj = MongoUser.objects.all()

    index_param = {
                    "user_info": userobj[0],
                   "skin_color": skin_color_dict,
                   }
    
    if userobj:
        return render(request, 'index.html', index_param)
#         return render(request, 'index.html', {"user": userobj[0]})
#         return render(request, 'base.html', {"user": userobj[0]})
    else:
        return redirect('login')

#    登陆系统，只用用户注册账号以后，管理员授权的账号方可登陆
def login(request):
    # 如果是POST请求，则说明是点击登录按扭 FORM表单跳转到此的，那么就要验证密码，并进行保存session
    if request.method == "POST":
        login_name = request.POST.get('login_name')
        password = request.POST.get('password')

        candidate_user = Candidate_user.objects.filter(login_name=login_name, password=password)
        
        if candidate_user:
            if candidate_user[0].account_status:
                # 登录成功
                # 1，生成特殊字符串
                # 2，这个字符串当成key，此key在数据库的session表（在数据库存中一个表名是session的表）中对应一个value
                # 3，在响应中,用cookies保存这个key ,(即向浏览器写一个cookie,此cookies的值即是这个key特殊字符）
                request.session['is_login'] = '1'  # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，即判断是否已经登录，用此判断）
                request.session['login_name'] = login_name  # 这个要存储的session是用于后面，每个页面上要显示出来，登录状态的用户名用。
                # 说明：如果需要在页面上显示出来的用户信息太多（有时还有积分，姓名，年龄等信息），所以我们可以只用session保存user_id
                
                print("--- " + login_name + " 登录系统 ---")
#                 user_id = str(candidate_user[0]._id)
#                 print(user_id)
                
                
                return redirect('index')
            else:
                return render(request, 'login.html', {'return_info':'您的账号还未开通，请联系管理员！'})
        else:
            return render(request, 'login.html', {'return_info':'用户不存在！'})
        
    # 如果是GET请求，就说明是用户刚开始登录，使用URL直接进入登录页面的
    return render(request, 'login.html')

#    登出系统
def logout(request):
    request.session['is_login'] = '0'
    request.session['login_name'] = ''
    
    return redirect('login')

#    获取登陆用户信息
def get_userInfo(request):
    
    if request.method == "GET":
        login_name = request.GET.get('login_name')
    
    user_obj = Candidate_user.objects.filter(login_name=login_name).as_pymongo()
    user_obj_dict = user_obj[0]
    
    if user_obj_dict.get('birthday'):
        birthday_string = user_obj_dict.get('birthday').date().isoformat()
        user_obj_dict.update({'birthday':birthday_string})
    
    if user_obj_dict.get('enter_time'):
        enter_time_string = user_obj_dict.get('enter_time').date().isoformat()
        user_obj_dict.update({'enter_time':enter_time_string})
    
    if user_obj_dict.get('create_time'):
        create_time_string = user_obj_dict.get('create_time').date().isoformat()
        user_obj_dict.update({'create_time':create_time_string})
    
    if user_obj_dict.get('dimission_time'):
        create_time_string = user_obj_dict.get('dimission_time').date().isoformat()
        user_obj_dict.update({'dimission_time':create_time_string})
    
    return render(request, 'user_html/show_user_info.html', user_obj_dict)

#    显示提示信息列表
def show_prompt_message(request):
    
    login_name = request.session.get('login_name')
    
#     user_obj = Candidate_user.objects.filter(login_name=login_name).as_pymongo()
#     result_json = user_obj.to_json(ensure_ascii=False)
#     print(result_json)
    
    prompt_message_obj = Candidate_user.objects(login_name=login_name).only('prompt_message').as_pymongo()
    
#     print(prompt_message_obj)
#     print(type(prompt_message_obj))
#     print(prompt_message_obj.to_json(ensure_ascii=False))
#     print(type(prompt_message_obj.to_json(ensure_ascii=False)))
#     prompt_message_json = prompt_message_obj.to_json(ensure_ascii=False)
    
    prompt_message_dict = prompt_message_obj[0]
    prompt_message_list = prompt_message_dict.get('prompt_message')
    
    result_count = 0
    read_count = 0
    unread_count = 0
    for one_message in prompt_message_list:
        if one_message['del_flag'] != 1:
            result_count += 1
            
            if one_message['read_status'] == 1:
                read_count += 1
            else:
                unread_count += 1
        else:
            continue
    
#     result_count = len(prompt_message_list)
#     print(result_count)
#     
#     unread_count = len(re.findall(r'"read_status": 0', result_json))
#     read_count = len(re.findall(r'"read_status": 1', result_json))
    
    result_json = dumps(prompt_message_list, ensure_ascii=False)
    print(result_json)
    
    result_dict = {
        'result_count':result_count,
        'read_count':read_count,
        'unread_count':unread_count,
        'result_json':result_json
    }
    
    return render(request, 'user_html/show-prompt-message.html', result_dict)

#    管理员提示用户注册授权
def prompt_register_authorize(request):
    
    admin_login_name = request.session.get('login_name')
    
    if request.method == "POST":
        register_login_name = request.POST.get('register_login_name')
        register_obj = Candidate_user.objects(login_name=register_login_name).update_one(account_status=True)
        
#         admin_obj = Candidate_user.objects(login_name=admin_login_name,prompt_message__S__login_name=register_login_name).update_one(set__prompt_message__S__read_status=1)
        admin_obj = Candidate_user.objects(login_name=admin_login_name, prompt_message__login_name=register_login_name).update_one(set__prompt_message__S__read_status=1)
#         admin_obj = Candidate_user.objects(login_name=admin_login_name).update_one({"$set":{'prompt_message.$.read_status':1}})
    
    status = 'success'
    
    return HttpResponse(status)

#    管理员提示信息删除
def prompt_message_del(request):
    
    admin_login_name = request.session.get('login_name')
    
    delete_count = 0
    status = 'false'
    for register_login_name, value in request.POST.items():
        if register_login_name:
            admin_obj = Candidate_user.objects(login_name=admin_login_name, prompt_message__login_name=register_login_name).update_one(set__prompt_message__S__del_flag=1)
            delete_count += 1
             
    if(delete_count):
        status = 'success'
    
#     return HttpResponse(status)
    return JsonResponse({'status': status, 'del_count': delete_count})

#    用户个人首页
@check_login
def iframe_welcome(request):

#     candidate_obj = Candidate_resource.objects[0:5]
#     candidate_obj = Candidate_resource.objects(company='美团', name='周璐')
#     data_list = list(candidate_obj)
#     total_count = len(data_list)
#     print('total:' + str(total_count))
#     print(Candidate_resource.objects.count())
#     
#     return render(request, 'welcome.html', {"user": candidate_obj[0]})
    return render(request, 'welcome.html')


#     user_id1 = request.session.get('user_id')
#      
#     user_id1 = '5bd038a76c92a52074dc29e3'
#     userobj = Candidate_user.objects.filter(_id=user_id1)
#  
#     #---    MongoDB
#     mongo_obj = Candidate_resource.objects.all()[0:10]
#      
#     if userobj:
# #         return render(request, 'welcome.html', {"user": userobj[0]})
#         return render(request, 'welcome.html', {"user": userobj[0], "mongo_info": mongo_obj[0]})
    
#-----------------------------------------------------------------------------------------------------------------------

#    管理员简历管理
def resume_manage(request):
    return render(request, 'talent_manage_html/resume_manage.html')

#    获取简历详细信息
def get_resumeInfo(request):
    
    resume_info_dict = {}
    if request.GET.get('telephone'):
        telephone = request.GET.get('telephone')
        
        resume_obj = Candidate_resource.objects.filter(telephone=telephone).as_pymongo()
        resume_info_dict = resume_obj[0]
        
        #********************************    前端控制显示排序    **************************
        remark_list = resume_info_dict.get('new_remark')
        #    根据dict的key排序list中的dict
        if remark_list:
            remark_list = sorted(remark_list, key = itemgetter('date_strf'),reverse = True)
            resume_info_dict.update({'new_remark': remark_list})
        #********************************    前端控制显示排序    **************************
    else:
        telephone = ""
        resume_info_dict.update({'telephone': telephone})
        
    
    #---    为了编辑简历信息，获取models中的所有字段，传到前端
    conn = MongoClient(host="127.0.0.1", port=27017)    #connect to mongodb
    db = conn.LMK_DB
    collection_data_dict = db.collection_data_dict
    collection_name = 'candidate_resource'
    filter_dict = {'collection_name': collection_name}
    result_dict = collection_data_dict.find_one(filter_dict)
    
    field_name_list_obj = Candidate_resource.__get_field_name__(Candidate_resource)
    field_name_list = field_name_list_obj.owner_document._fields_ordered
    
    all_fields_dict = {}
    for field_name in field_name_list:
        if re.search(r"_id", field_name):
            continue
    
        if result_dict['en_ch_dict'][field_name]:
            ch_field_name = result_dict['en_ch_dict'][field_name]
#             print(field_name + " = " + ch_field_name)
            all_fields_dict.update({field_name: ch_field_name})
    
    return_dict = {}
    if all_fields_dict:
        #    很多字段不需要在页面显示，需要pop掉，而且需要把必须的主要字段位移到数组的前面
        all_fields_dict.pop('first_uploader')
        all_fields_dict.pop('first_upload_time')
        all_fields_dict.pop('last_operator')
        all_fields_dict.pop('update_time')
        all_fields_dict.pop('new_import_flag')
        all_fields_dict.pop('del_flag')
        all_fields_dict.pop('new_remark')
        
        return_dict.update({'all_fields_dict': all_fields_dict})
        
    if resume_info_dict:
        if telephone:
            resume_info_dict.pop('_id')
            
        return_dict.update({'resume_info_dict': resume_info_dict})
    
    return render(request, 'talent_manage_html/show_resume_info.html', return_dict)

#    简历备注添加
def resume_remark_add(request):
    filter_params_dict = {}
    update_params_dict = {}
    
    if request.method == "POST":
    
        for key, value in request.POST.items():
            if key == 'telephone':
                value = int(value)
                print(type(value))
                filter_params_dict.update({key: value})
            else:
                if value:
                    update_params_dict.update({key: value})
                else:
                    update_params_dict.update({key: ''})
        
        conment = update_params_dict.pop('new_remark')
        print(conment)
        
        #    时间戳
        date_strf = time.time()
        #    格式化时间
        format_time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        #    最近的操作者
        last_operator_login_name = request.session.get('login_name')
        
        update_params_dict.update({'update_time':format_time_string, 'last_operator':last_operator_login_name})
        
        print(filter_params_dict)
        print(update_params_dict)
        
        status = 'error'
        if filter_params_dict:
            if conment != '':
                one_remark = One_remark(comment=conment, date_strf=date_strf, date_string=format_time_string, last_operator=last_operator_login_name)
    #             candidate_obj = Candidate_resource.objects(**filter_params_dict).update(push__new_remark=one_remark)
                candidate_obj = Candidate_resource.objects(**filter_params_dict).update(upsert= True, **update_params_dict, push__new_remark=one_remark)
                if candidate_obj:
                    status = 'success'
            
    
        return JsonResponse({'status': status})
        
#         for register_login_name, value in request.POST.items():
#             if register_login_name:
#                 admin_obj = Candidate_user.objects(login_name=admin_login_name, prompt_message__login_name=register_login_name).update_one(set__prompt_message__S__del_flag=1)
#                 delete_count += 1
#                   
#         if(delete_count):
#             status = 'success'
#         
#         return HttpResponse("success")
#         return JsonResponse({'status': status, 'del_count': delete_count})
    else:
        telephone = request.GET.get('telephone')
        return render(request, 'talent_manage_html/resume_remark_add.html',{'telephone':telephone})

#    根据检索条件，统计数据条数
def get_total_count(request):
    filter_params_dict = {}
    for key, value in request.GET.items():
        if value:
            key = key + '__icontains'
            filter_params_dict.update({key: value})

#     if filter_params_dict:
#         candidate_obj = CandidateResource.objects.filter(**filter_params_dict).values('name', 'telephone', 'company', 'position', 'new_remark')
#     else:
#         candidate_obj = CandidateResource.objects.all().values('name', 'telephone', 'company', 'position')
    
#     candidate_obj = Candidate_resource.objects(company='美团', name='周璐')
#     candidate_obj = Candidate_resource.objects(**filter_params_dict)
#     if filter_params_dict:
#         candidate_obj = Candidate_resource.objects(**filter_params_dict)
#     else:
#         candidate_obj = Candidate_resource.objects.all()

    if filter_params_dict:
        candidate_obj = Candidate_resource.objects(**filter_params_dict)
        data_list = list(candidate_obj)
        total_count = len(data_list)
    else:
        total_count = Candidate_resource.objects.count()
    
    print('total:' + str(total_count))
    return HttpResponse(total_count)

#    检索简历
def search_jianli(request):
    filter_params_dict = {}
    pagination_params_dict = {}

    for key, value in request.GET.items():
        print(key + ':' + value)
        if re.search('page', key, flags=0):
            pagination_params_dict.update({key:value})
        else:
            if value:
                key = key + '__icontains'
                filter_params_dict.update({key:value})

    print(filter_params_dict)
    print(pagination_params_dict)

    per_page_count = int(pagination_params_dict.get('per_page_count'))

    from_search_count = 0
    if pagination_params_dict.get('current_page_num'):
        current_page_num = int(pagination_params_dict.get('current_page_num')) - 1
        from_search_count = per_page_count * current_page_num

#     if filter_params_dict:
#         # candidate_obj = CandidateResource.objects.filter(company='美团', name='周璐').values('name', 'telephone', 'company')[:10]
#         # candidate_obj = CandidateResource.objects.filter(**filter_params_dict)[0:1]   #---    这种方式报错
#         candidate_obj = CandidateResource.objects.filter(**filter_params_dict).values('name', 'telephone', 'company', 'position', 'new_remark')[from_search_count:from_search_count + 10]
#     else:
#         candidate_obj = CandidateResource.objects.all().values('name', 'telephone', 'company', 'position', 'new_remark')[from_search_count:from_search_count + 10]

    collection_obj = Candidate_resource.objects(**filter_params_dict)[0:1]
    candidate_obj = collection_obj._collection_obj.find(collection_obj._query, sort=[("update_time",pymongo.DESCENDING)])[from_search_count:from_search_count + 10]
    
#     if filter_params_dict:
#         candidate_obj = Candidate_resource.objects(**filter_params_dict)[from_search_count:from_search_count + 10]
#     else:
# #         candidate_obj = Candidate_resource.objects.all()[from_search_count:from_search_count + 10]
#         candidate_obj = Candidate_resource.objects[from_search_count:from_search_count + 10]
#     
#     data_list = list(candidate_obj)
    
#     print(len(data_list))
#     for user in candidate_obj:
#         print(user.name)

    
#     data_json = data_list.to_json()
#     data_json = serializers(data_list)
#     data_json = json.dumps(data_list, ensure_ascii=False)

    data_json = dumps(candidate_obj, ensure_ascii=False)
#     data_json = serializers.serialize('json', candidate_obj, ensure_ascii=False)
    print(data_json)#-----------------------------------

    return HttpResponse(data_json)

#    添加简历
def insert_jianli(request):
#     filter_params_dict = {}
#     update_params_dict = {}

    login_name = request.session.get('login_name')
    
    insert_params_dict = {}
    for key, value in request.POST.items():
        if value:
                insert_params_dict.update({key: value})
    
        #    时间戳
    date_strf = time.time()
    #    格式化时间
    format_time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
    insert_params_dict.update({'first_uploader': login_name, 'first_upload_time': format_time_string})
    insert_params_dict.update({'last_operator': login_name, 'update_time': format_time_string})
    insert_params_dict.update({'new_import_flag': 1})
    
#     for key, value in request.GET.items():
#         if key == 'telephone':
#             value = int(value)
#             print(type(value))
#             filter_params_dict.update({key: value})
#         else:
#             if value:
#                 # print(key + ':' + value)
#                 update_params_dict.update({key: value})
#             else:
#                 update_params_dict.update({key: ''})

#     conment = update_params_dict['new_remark']
#     conment = update_params_dict.pop('new_remark')
#     print(conment)
#     
#     conment= ''
#     print(filter_params_dict)
#     print(update_params_dict)
#     
#     #    时间戳
#     date_strf = time.time()
#     #    格式化时间
#     format_time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
# 
#     status = 'error'
#     if filter_params_dict:
#         if(conment != ''):
#             one_remark = One_remark(comment=conment, date_strf=date_strf, date_string=format_time_string)
#             candidate_obj = Candidate_resource.objects(**filter_params_dict).update(upsert= True, **update_params_dict, push__new_remark=one_remark)
#             if candidate_obj:
#                 status = 'success'
#         else:
#             candidate_obj = Candidate_resource.objects(**filter_params_dict).update(upsert= True, **update_params_dict)
#             candidate_obj = Candidate_resource.objects(**insert_params_dict).insert()
#             if candidate_obj:
#                 status = 'success'

    if insert_params_dict:
        print(insert_params_dict)
#         candidate_obj = Candidate_resource.objects.insert(**insert_params_dict)
#         candidate_obj = Candidate_resource(**insert_params_dict)  
#         candidate_obj.insert()
        candidate_obj = Candidate_resource.objects.create(**insert_params_dict)
        if candidate_obj:
                status = 'success'
    
    return JsonResponse({'status': status})

#-----------------------------------------------------------------------------------------------------------------------

#    更新简历
def update_jianli(request):
    filter_params_dict = {}
    update_params_dict = {}
    login_name = request.session.get('login_name')

    for key, value in request.POST.items():
        if key == 'telephone':
            value = int(value)
            print(type(value))
            
            
            if value:
                filter_params_dict.update({key: value})
                update_params_dict.update({key: value})
        else:
            if value:
                # print(key + ':' + value)
                update_params_dict.update({key: value})
            else:
                update_params_dict.update({key: ''})

#     conment = update_params_dict['new_remark']
#     conment = update_params_dict.pop('new_remark')
#     print(conment)
    
    print(filter_params_dict)
    print(update_params_dict)
    
    #    时间戳
    date_strf = time.time()
    #    格式化时间
    format_time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    update_params_dict.update({'last_operator': login_name, 'update_time': format_time_string})
    update_params_dict.update({'new_import_flag': 0})
    
    status = 'error'
    if filter_params_dict:
#         candidate_obj = CandidateResource.objects.filter(**filter_params_dict).update(**update_params_dict)
        
#         candidate_resource.update(filter_params_dict, {"$set":update_params_dict,
#                                                     "$push":{"new_remark":{
#                                                                                    "comment" : "1101更新数据和更新内嵌文档都已经好用了",
#                                                                                    "date_strf":date_strf,
#                                                                                    "date_string":format_time_string
#                                                                                    }}})
        
        candidate_obj = Candidate_resource.objects(**filter_params_dict).update(upsert= True, **update_params_dict)
        if candidate_obj:
            status = 'success'
        
#         if(conment != ''):
#             one_remark = One_remark(comment=conment, date_strf=date_strf, date_string=format_time_string)
# #             candidate_obj = Candidate_resource.objects(**filter_params_dict).update(push__new_remark=one_remark)
#             candidate_obj = Candidate_resource.objects(**filter_params_dict).update(upsert= True, **update_params_dict, push__new_remark=one_remark)
#             if candidate_obj:
#                 status = 'success'
        

    return JsonResponse({'status': status})
#-----------------------------------------------------------------------------------------------------------------------

#    管理员权限显示
def admin_permission(request):
    permission_obj = Permission.objects.as_pymongo()
    
    result_json = dumps(permission_obj, ensure_ascii=False)
    print(result_json)
    
    result_count = Permission.objects.count()
    result_dict = {
        'result_count':result_count,
        'result_json':result_json
    }
    return render(request, 'admin_html/admin-permission.html', result_dict)

#    管理员权限添加
def admin_permission_add(request):
    filter_params_dict = {}
    update_params_dict = {}
    
    if request.method == "POST":
        for key, value in request.POST.items():
            if key == 'old-permission-name':
                filter_params_dict.update({'permission_name': value})
            else:
                update_params_dict.update({key: value})
                    
        if update_params_dict:
            if filter_params_dict:
                permission_obj = Permission.objects(**filter_params_dict).update(upsert= True, **update_params_dict)
            else:
                permission_obj = Permission(**update_params_dict)
                permission_obj.save()
            
            status = 'success'
            return HttpResponse(status)
        else:
            return render(request, 'admin_html/admin-permission-add.html')
    else:
        type = ''
        for key, value in request.GET.items():
            if key == 'type':
                type = value
            else:
                update_params_dict.update({key: value})
    
        if type:
            return render(request, 'admin_html/admin-permission-add.html', update_params_dict)
        else:
            return render(request, 'admin_html/admin-permission-add.html')

#    管理员权限删除
def admin_permission_del(request):
    
    delete_count = 0
    status = 'false'
    for permission_name, value in request.POST.items():
        if permission_name:
            Permission.objects(permission_name=permission_name).delete()
            delete_count += 1
             
    if(delete_count):
        status = 'success'
    
    return HttpResponse(status)

#    显示管理员角色列表
def admin_role(request):
#     role_obj = Role.objects.all()
    
    role_obj = Role.objects.order_by('role_level').as_pymongo()
    
    result_json = dumps(role_obj, ensure_ascii=False)
    print(result_json)
    
    result_count = Role.objects.count()
    result_dict = {
        'result_count':result_count,
        'result_json':result_json
    }
    return render(request, 'admin_html/admin-role.html', result_dict)

#    管理员角色添加
def admin_role_add(request):
    filter_params_dict = {}
    update_params_dict = {}
    
    type = ''
    for key, value in request.GET.items():
        if key == 'type':
            type = value
        else:
            update_params_dict.update({key: value})
#             if value:
#                 update_params_dict.update({key: value})
#             else:
#                 update_params_dict.update({key: ''})

    if type:
        return render(request, 'admin_html/admin-role-add.html', update_params_dict)
    
    for key, value in request.POST.items():
        if key == 'old-role-name':
            filter_params_dict.update({'role_name': value})
        else:
            update_params_dict.update({key: value})
                
    if update_params_dict:
#         role_obj = Role.objects.update(upsert= True, **update_params_dict)
        
        if filter_params_dict:
            role_obj = Role.objects(**filter_params_dict).update(upsert= True, **update_params_dict)
        else:
            role_obj = Role(**update_params_dict)
            role_obj.save()
        
        
        status = 'success'
        return HttpResponse(status)
    else:
        return render(request, 'admin_html/admin-role-add.html')

#    管理员角色删除
def admin_role_del(request):
    
    delete_count = 0
    status = 'false'
    for role_name, value in request.POST.items():
        if role_name:
            Role.objects(role_name=role_name).delete()
            delete_count += 1
             
    if(delete_count):
        status = 'success'
    
    return HttpResponse(status)

#    显示用户列表
def show_user_list(request):
    user_obj = Candidate_user.objects(del_flag__ne=1).order_by('-role_name').as_pymongo()
    
    result_json = dumps(user_obj, ensure_ascii=False)
    print(result_json)
    
    result_count = user_obj.count()
    result_dict = {
        'result_count':result_count,
        'result_json':result_json
    }
    return render(request, 'admin_html/user-list.html', result_dict)

#    用户账号开关
def user_account_switch(request):
    
    real_name = request.POST.get('real_name')
    switch_flag = int(request.POST.get('switch_flag'))
    
    account_statu = False
    if switch_flag:
        account_statu = True
    
    if real_name:
        user_obj = Candidate_user.objects(real_name=real_name).update_one(set__account_status=account_statu)
             
    if(user_obj):
        status = 'success'
    
#     return HttpResponse(status)
    return JsonResponse({'status': status})

#    删除用户
def user_del(request):
    
    delete_count = 0
    status = 'false'
    for real_name, value in request.POST.items():
        if real_name:
            user_obj = Candidate_user.objects(real_name=real_name).update_one(set__del_flag=1)
            delete_count += 1
             
    if(delete_count):
        status = 'success'
    
#     return HttpResponse(status)
    return JsonResponse({'status': status, 'del_count': delete_count})

# 
# from .forms import UserForm
# from .views_mongo import import_one_resume
# from lmk_app.lmk_tools.resume_tools.read_file_word import read_word
# #    简历导入
# def resume_import(request):
#     login_name = request.session.get('login_name')
#     
#     if request.method == 'POST':
#         userform = UserForm(request.POST, request.FILES)
#         
#         resume_file = request.FILES.get("upload", None)    # 获取上传的文件，如果没有文件，则默认为None
#         
# #         if resume_file.is_valid():
#         
#         if resume_file:
#             print(resume_file.name)
#             text = resume_file.read()
#             print(sys.getdefaultencoding())
#             print(text)
# #             string = text.decode()
# #             print(string)
#             
# #         resume_file_path = 
#         
#         if not resume_file:
#             print('file none')
# #             return HttpResponse("no files for upload!")  
#         else:
#             return HttpResponse("upload over!")
#     else:
#         userform = UserForm(initial ={'userName': login_name})
#         return render(request, 'tools_html/resume_import.html', {'userform': userform})
# #     return render_to_response('tools_html/resume_import.html',{'uf':uf})
# #     return render(request, 'tools_html/resume_import.html')
#############下面是公司模块后台代码###################################################
def company_list(request):#公司展示
#     return render(request, 'admin_html/admin-role-add.html')
        return render(request, 'client_html/company_html/company_list.html')
    ########公司列表修改内容#################
def company_ajax(request):#公司展示ajax 不传参
#     query_set= new_company.objects.filter(flags=1) 过滤掉已经删除的数据
    end = None 
    start = None
    page = request.GET.get('page')   
    PageSize = 10,
    N = int(page)*PageSize # n = 20
    CD_obj = new_company.objects.order_by('server').as_pymongo()
    value_count = CD_obj.count() #16
    if  value_count > N:
        end = N
        start = N-10
    elif N-10<value_count<N:
        end = value_count
        start = N-10
    data_obj = CD_obj[start:end]
    all_value=dumps(data_obj, ensure_ascii=False)
    
    return JsonResponse({'data_count': value_count, 'data': all_value})
def list_exid(request):
    filter_params_dict = {}
    update_params_dict = {}
    status="error"
    
    for key, value in request.POST.items():
        print(key)
        key_list=key.split("[")
        new_key=(key_list[2])[:-1]
        print(value)
        if new_key=="ID":
            filter_params_dict.update({new_key: value})
        else:
            update_params_dict.update({new_key: value})
    print(filter_params_dict)
    print(update_params_dict)
    company_obj = new_company.objects(update_params_dict).update(upsert= True, **update_params_dict)    
            
    print("11111")
    status="success"
    return JsonResponse({'status': status})
##################公司列表删除内容#########################
def list_del(request):
    status="error"
    filter_params_dict = {}
    update_params_dict = {}
    company_name=request.POST.get("company_name")
    print(company_name)
    if company_name!="":
        filter_params_dict.update({"company_name":company_name})
        update_params_dict.update({"flags":0})
        company_obj = new_company.objects(**filter_params_dict).update(upsert= True, **update_params_dict) 
        if company_obj:
            status="success"
        
    return JsonResponse({'status': status})
#####################搜索展示内容###############################
def search_ajax(request):
    status = SystemContants.ErrorStatus
    search_text=request.POST.get("search_text")
    print(search_text)
    search_list=search_text.split(":")
    key=search_list[0]
    value=search_list[1]
    print(key)
    print(value)
    if key=="search_chendian":
        query_set= new_company.objects.filter(company_name=value)
        commpany_list= query_set._collection_obj.find(query_set._query)
        print(commpany_list)
        data_json=dumps(commpany_list, ensure_ascii=False)
        print(data_json)
        print(111)
        return HttpResponse(data_json)
    if key=="search_industy":
        query_set= new_company.objects.filter(industry=value)
        commpany_list= query_set._collection_obj.find(query_set._query)
        print(commpany_list)
        data_json=dumps(commpany_list, ensure_ascii=False)
        print(data_json)
        print(111)
        return HttpResponse(data_json)
    if key=="search_server":
        query_set= new_company.objects.filter(server=value)
        commpany_list= query_set._collection_obj.find(query_set._query)
        print(commpany_list)
        data_json=dumps(commpany_list, ensure_ascii=False)
        print(data_json)
        print(111)
        return HttpResponse(data_json)
    if key=="search_class":
        query_set= new_company.objects.filter(company_class=value)
        commpany_list= query_set._collection_obj.find(query_set._query)
        print(commpany_list)
        data_json=dumps(commpany_list, ensure_ascii=False)
        print(data_json)
        print(111)
        return HttpResponse(data_json)
def business_add(request): 
    '''
        定义一个 状态 error
        
    '''
    status="error"
#     content_list=[]
    company_dict={}
#     content_dict={}
    for key, value in request.POST.items():
        #解析前台传递的列表数据,例如base_info[0]company_name变成company_name  与数据库对应
        print(key +"[:]"+ value)
        if value == '' or '选择' in value:
            value = None
        company_dict.update({key: value})
        login_name = request.session.get('login_name')
        random_data = "".join(map(lambda x:random.choice(string.digits), range(8)))
        company_dict.update({'ID': random_data,'flags':'1','person' : login_name})
        Method = StrMehod.StrMethod()
        location_time = Method.format_time_to_str()
        company_dict.update({SystemContants.CreatTime:location_time,SystemContants.UpdateTime:location_time})
 

#         if "content_info" in key:
#             key_list=key.split("[")
#             key1=(key_list[1])[:-1]
#             print(key1)
#             key2=(key_list[2])[:-1]
#             new_key=key2
#             if "new_contectsRemark" in new_key:
#                 content_dict.update({new_key:value}) 
#                 content_list.append(content_dict)
#                 content_dict={}
#             # 最后一个遍历结束把包含所有联系人的字典添加到列表中
#             else:
#                 content_dict.update({new_key:value}) 
#     if content_list !=[]:     
#         company_dict.update({"new_contects":content_list})
#         print(company_dict)

    if company_dict =={}:#判断是不是添加按钮之后进的后台
        yx_server_list = []
        value_list= SingleValue.objects.order_by('-codetype').as_pymongo()
        all_value=dumps(value_list, ensure_ascii=False)
        server_info = SwaggerCommon.objects.as_pymongo()
        for item in server_info:
            server = item.get(DataBaseFeildContants.ServerKey)
            if server:
                if server not in  yx_server_list:
                    yx_server_list.append(server)
        print(yx_server_list)
        server_count = len(yx_server_list)
        value_count = value_list.count()
        result_data = {
            'all_value':all_value,
            'value_count':value_count,
            'server_list':yx_server_list,
            'server_count':server_count
            }
        
        return render( request,'client_html/company_html/business_add.html',result_data)
    else :
        name = company_dict['CD_name']
        query_set= new_company.objects.filter(CD_name=name).order_by('-ID').as_pymongo()
        if query_set:
            return HttpResponse(status)
        else:
            company_obj = new_company(**company_dict)
            company_obj.save()
            print("保存成功")
            status='success'        
            return HttpResponse(status)
#         if "company_name" in company_dict:
#             global company_name
#             company_name=company_dict["company_name"]
#             print(company_name)
#         new_contectsName=company_dict.pop("new_contectsName")
#         new_contectsJob=company_dict.pop("new_contectsJob")
#         new_contectsTel=company_dict.pop("new_contectsTel")
#         new_contectsEmall=company_dict.pop("new_contectsEmall")
#         new_contectsLine=company_dict.pop("new_contectsLine")
#         new_contectsOther=company_dict.pop("new_contectsOther")
#         new_contectsRemark=company_dict.pop("new_contectsRemark")
#         company_obj = new_company(**company_dict)
#         company_obj.save()
#        
#         
#         print('保存成功')
#         query_set=new_company.objects.filter(company_name=company_name)#等号前面是数据库的字段名称，后面是传值
#         print(query_set)
#         
#         NewContect_dict =query_set._collection_obj.find(query_set._query)
#         data_json=dumps(NewContect_dict, ensure_ascii=False)
#         remark_dict=(json.loads(data_json))[0]
#         del remark_dict['_id']
#         comment_new = remark_dict.pop("new_contects")
#         New_contect = new_contect(new_contectsName=new_contectsName,
#                                          new_contectsJob=new_contectsJob, 
#                                          new_contectsTel=new_contectsTel,
#                                          new_contectsEmall=new_contectsEmall,
#                                          new_contectsLine=new_contectsLine,
#                                          new_contectsOther=new_contectsOther,
#                                          new_contectsRemark=new_contectsRemark
#                                          )
#         candidate_obj = new_company.objects(**remark_dict).update(upsert= True, **remark_dict, push__new_contects=New_contect)
#         print(candidate_obj)
#         status='success'
#         return HttpResponse(status)


#    
#             
#  
def add_contects(request):
    update_params_dict = {}
    status='error'
 
    type = ''
     
    print(request.GET.items)
    for key, value in request.GET.items():
        if key =='company_name':
            global company_name#声明全局变量
            company_name=value#赋值
 
 
      
        else:
             
            update_params_dict.update({key: value})
    print(update_params_dict)
     
    if "new_contectsName" in update_params_dict :
            query_set=new_company.objects.filter(contacts_name=company_name)#等号前面是数据库的字段名称，后面是传值
            print(query_set)
            NewContect_dict =query_set._collection_obj.find(query_set._query)
            data_json=dumps(NewContect_dict, ensure_ascii=False)
            remark_dict=(json.loads(data_json))[0]
            del remark_dict['_id']
            comment_new = remark_dict.pop("new_contects")
            new_contectsName =update_params_dict.get('new_contectsName')
            print(new_contectsName)
            new_contectsJob=update_params_dict.get('new_contectsJob')
            new_contectsTel=update_params_dict.get('new_contectsTel')
            new_contectsEmall=update_params_dict.get('new_contectsEmall')
            new_contectsLine=update_params_dict.get('new_contectsLine')
            new_contectsOther=update_params_dict.get('new_contectsOther')
            new_contectsRemark=update_params_dict.get('new_contectsRemark')
            if new_contectsName !='':
                New_contect = new_contect(new_contectsName=new_contectsName,
                                         new_contectsJob=new_contectsJob, 
                                         new_contectsTel=new_contectsTel,
                                         new_contectsEmall=new_contectsEmall,
                                         new_contectsLine=new_contectsLine,
                                         new_contectsOther=new_contectsOther,
                                         new_contectsRemark=new_contectsRemark
                                         )
                candidate_obj = new_company.objects(**remark_dict).update(upsert= True, **remark_dict, push__new_contects=New_contect)
                print(candidate_obj)
                 
                status="success"
                return HttpResponse(status)
    return render(request,'client_html/company_html/add_contects.html')
   
# ##############################################下面是职位模块代码########################################
def position_add(request):
    position_dict={}
    status='error'
    for key, value in request.POST.items():
        if key:
            print(value)
            position_dict.update({key: value})
     
     
    if position_dict =={}:#判断是不是添加按钮之后进的后台
        return render(request, 'client_html/position_html/position_add.html')
    else:
        min_salary = position_dict.pop("min_salary")
        max_salary = position_dict.pop("max_salary")
        salary_range = min_salary+"-"+ max_salary
        position_class = position_dict.pop("position_class")
        second_class = position_dict.pop("second_class")
        salary_range = min_salary+"-"+ max_salary
        position_class =position_class +"->"+second_class
        print(salary_range)
        print(position_class)
        position_dict.update({"salary_range": salary_range})
        position_dict.update({"position_class": position_class})
        print(position_dict)
        position_obj = position_info(**position_dict)
        position_obj.save()
        print("保存成功")
        status='success'
    return HttpResponse(status)
def newCompany_ajax(request):
    query_set= new_company.objects.all()
    commpany_list= query_set._collection_obj.find(query_set._query)
    print(commpany_list)
     
    data_json=dumps(commpany_list, ensure_ascii=False)
    print(data_json)
    print(111)
    return HttpResponse(data_json)
#获取所有一级分类的信息
def frist_class(request):
    classes=position_classification.objects.all()
    print(classes)
    print(11111)
    classification_list= classes._collection_obj.find(classes._query)
    data_json=dumps(classification_list, ensure_ascii=False)
    return HttpResponse(data_json)
#获取用后下拉菜单
def users_select(request):
    users= Candidate_user.objects.all()
    print(users)
    print(11111)
    users_list= users._collection_obj.find(users._query)
    data_json=dumps(users_list, ensure_ascii=False)
    return HttpResponse(data_json)
def position_list(request):
    return render(request, 'client_html/position_html/position_list.html')
def position_ajax(request):
    query_set= position_info.objects.all()
    position_list= query_set._collection_obj.find(query_set._query)
    print(position_list)
    data_json=dumps(position_list, ensure_ascii=False)
    print(data_json)
    print(111)
    return HttpResponse(data_json)
# # def x_exidtable(request):
# #     position_dict={}
# #     status='error'
# #     for key, value in request.POST.items():
# #         if key:
# #             print(value)
# #             position_dict.update({key: value})
# #     return render(request, 'client_html/company_html/x_exidtable.html')
def company_info(request):
    #公司信息
    for key, value in request.GET.items():
        if key=="company_name":
            global company_name
            company_name=value
            print(company_name)
            return render(request, 'client_html/company_html/company_info.html')
    query_set=new_company.objects.filter(company_name=company_name)
    if query_set:
        company_info= query_set._collection_obj.find(query_set._query)
        data_json=dumps(company_info, ensure_ascii=False)
        print(data_json)
        print(111)
        return HttpResponse(data_json)
     
    return render(request, 'client_html/company_html/company_info.html')
#公司修改
def company_exid(request):
    filter_params_dict = {}
    one_params_dict={}
    update_params_dict = {}
    status='error'
    for key, value in request.POST.items():
        if "exid_list" in key:
            key_list=key.split("[")# exid_list,0],company_name]
            key2=(key_list[2])[:-1]#company_name
            one_params_dict.update({key2: value})
        if key=="company_name":
            global company_name
            company_name=value
    if  one_params_dict!={}:
        query_set=new_company.objects.filter(company_name=company_name)
        company_info= query_set._collection_obj.find(query_set._query)
        data_json=dumps(company_info, ensure_ascii=False)
        company_dict=(json.loads(data_json))[0]
        #del company_dict['_id']
        print(company_dict)
         
        dict_key=company_dict.keys()
        one_key=one_params_dict.keys()
        #判断是第几个联系人
        for i in one_key:
            if i in dict_key:
                update_params_dict.update(i,one_params_dict[i])
            # company_dict.update({i:item})
            else :
                index=int(i[-1])
                
                contect=company_dict['new_contects']
                contect_dict=contect[index]
                if i[:-1] in contect_dict:
                    new_key=i[:-1]
                    contect_dict.update({new_key:one_params_dict[i]})
                    contect[index]=contect_dict
                update_params_dict.update({"new_contects":contect})
               
             
        print(update_params_dict)
        filter_params_dict.update({"company_name":company_name})
        print(filter_params_dict)
        company_obj = new_company.objects(**filter_params_dict).update(upsert= True, **update_params_dict)
         
        print(11111)
    return HttpResponse(status)
#     
# =======
# >>>>>>> .r225

    


