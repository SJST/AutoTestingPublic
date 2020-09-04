
# from lmk_app_backup.models import Candidate_resource
import os
import sys
import importlib
importlib.reload(sys)

from lmk_app_backup import Candidate_user
from lmk_app_backup import Candidate_resource
from lmk_app_backup import One_remark, One_prompt
from lmk_app_backup import Skin_color
from lmk_app_backup import Role, Permission
import time
from datetime import date
import re
from bson.json_util import dumps
import json
from django.template.context_processors import request

try:
    from django.http import JsonResponse
except ImportError:
    from lmk_app_backup import JsonResponse

from functools import wraps
from django.shortcuts import render, render_to_response, redirect, HttpResponse

#    鏂扮敤鎴锋敞鍐岋紝娉ㄥ唽涔嬪悗绛夊緟绠＄悊鍛樺鎵规巿鏉�
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
                        #    鐢╰ime妯″潡    print (timeArray.tm_year)    #2018
                        #    print (timeArray )    #time.struct_time(tm_year=2018, tm_mon=12, tm_mday=3, tm_hour=20, tm_min=40, tm_sec=0, tm_wday=0, tm_yday=337, tm_isdst=-1)
                        time_array = time.strptime(value, "%Y-%m-%d")
                        time_strp = int(time.mktime(time_array))
                        time_iso_obj = date.fromtimestamp(time_strp)
                        
#                         #    鐢╠atetime妯″潡    print (datetimeArray.year) #2018
#                         datetimeArray=datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
#                         timeStamp1=time.mktime(datetimeArray.timetuple())
                        print(key)
                        print(value)
                        print(time_array)
                        print(time_strp)
                        
                        #    闇�瑕佹妸鏃堕棿鎴宠浆鎹㈡垚date瀵硅薄锛屾墠鑳藉瓨鍏ongodb涓�
                        update_params_dict.update({key: time_iso_obj})
            else:
                if value:
                    update_params_dict.update({key: value})
                    
        if update_params_dict:
            candidate_obj = Candidate_user(**update_params_dict)
            candidate_obj.save()
            
            #    鏃堕棿鎴�
            date_strf = time.time()
            #    鏍煎紡鍖栨椂闂�
            format_time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            one_prompt = One_prompt(login_name=update_params_dict['login_name'], register_real_name=update_params_dict['real_name'], date_strf=date_strf, date_string=format_time_string)
            
            admin_prompt_update_obj = Candidate_user.objects(role_name__endswith="绠＄悊鍛�").update(upsert= True, push__prompt_message=one_prompt)
#             super_prompt_update_obj = Candidate_user.objects(real_name="鐜嬩负鍐�").update(upsert= True, push__prompt_message=one_prompt)
            
            if admin_prompt_update_obj:
                print("success add a prompt message")
            else:
                print("failed add a prompt message")
            
            status = 'success'
            return HttpResponse(status)
        
    return render(request, 'register.html')

# 璇存槑锛氳繖涓楗板櫒鐨勪綔鐢紝灏辨槸鍦ㄦ瘡涓鍥惧嚱鏁拌璋冪敤鏃讹紝閮介獙璇佷笅鏈夋病娉曟湁鐧诲綍锛�
# 濡傛灉鏈夎繃鐧诲綍锛屽垯鍙互鎵ц鏂扮殑瑙嗗浘鍑芥暟锛�
# 鍚﹀垯娌℃湁鐧诲綍鍒欒嚜鍔ㄨ烦杞埌鐧诲綍椤甸潰銆�
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

#    鐢ㄦ埛鐧婚檰涔嬪悗鐨勭晫闈紝鏍规嵁鐢ㄦ埛瑙掕壊鍐冲畾椤甸潰鍔熻兘鐨勬樉绀�
@check_login
def index(request):
    # return render(request, 'test_index.html')

#     user_id = request.session.get('user_id')
    login_name = request.session.get('login_name')
#     user_id = '5bd038a76c92a52074dc29e3'

    # 浣跨敤user_id鍘绘暟鎹簱涓壘鍒板搴旂殑user淇℃伅
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

#    鐧婚檰绯荤粺锛屽彧鐢ㄧ敤鎴锋敞鍐岃处鍙蜂互鍚庯紝绠＄悊鍛樻巿鏉冪殑璐﹀彿鏂瑰彲鐧婚檰
def login(request):
    # 濡傛灉鏄疨OST璇锋眰锛屽垯璇存槑鏄偣鍑荤櫥褰曟寜鎵� FORM琛ㄥ崟璺宠浆鍒版鐨勶紝閭ｄ箞灏辫楠岃瘉瀵嗙爜锛屽苟杩涜淇濆瓨session
    if request.method == "POST":
        login_name = request.POST.get('login_name')
        password = request.POST.get('password')

        candidate_user = Candidate_user.objects.filter(login_name=login_name, password=password)
        
        if candidate_user:
            if candidate_user[0].account_status:
                # 鐧诲綍鎴愬姛
                # 1锛岀敓鎴愮壒娈婂瓧绗︿覆
                # 2锛岃繖涓瓧绗︿覆褰撴垚key锛屾key鍦ㄦ暟鎹簱鐨剆ession琛紙鍦ㄦ暟鎹簱瀛樹腑涓�涓〃鍚嶆槸session鐨勮〃锛変腑瀵瑰簲涓�涓獀alue
                # 3锛屽湪鍝嶅簲涓�,鐢╟ookies淇濆瓨杩欎釜key ,(鍗冲悜娴忚鍣ㄥ啓涓�涓猚ookie,姝ookies鐨勫�煎嵆鏄繖涓猭ey鐗规畩瀛楃锛�
                request.session['is_login'] = '1'  # 杩欎釜session鏄敤浜庡悗闈㈣闂瘡涓〉闈紙鍗宠皟鐢ㄦ瘡涓鍥惧嚱鏁版椂瑕佺敤鍒帮紝鍗冲垽鏂槸鍚﹀凡缁忕櫥褰曪紝鐢ㄦ鍒ゆ柇锛�
                request.session['login_name'] = login_name  # 杩欎釜瑕佸瓨鍌ㄧ殑session鏄敤浜庡悗闈紝姣忎釜椤甸潰涓婅鏄剧ず鍑烘潵锛岀櫥褰曠姸鎬佺殑鐢ㄦ埛鍚嶇敤銆�
                # 璇存槑锛氬鏋滈渶瑕佸湪椤甸潰涓婃樉绀哄嚭鏉ョ殑鐢ㄦ埛淇℃伅澶锛堟湁鏃惰繕鏈夌Н鍒嗭紝濮撳悕锛屽勾榫勭瓑淇℃伅锛夛紝鎵�浠ユ垜浠彲浠ュ彧鐢╯ession淇濆瓨user_id
                
                user_id = str(candidate_user[0]._id)
                print(user_id)
                
                
                return redirect('index')
            else:
                return render(request, 'login.html', {'return_info':'鎮ㄧ殑璐﹀彿杩樻湭寮�閫氾紝璇疯仈绯荤鐞嗗憳锛�'})
        else:
            return render(request, 'login.html', {'return_info':'鐢ㄦ埛涓嶅瓨鍦紒'})
        
    # 濡傛灉鏄疓ET璇锋眰锛屽氨璇存槑鏄敤鎴峰垰寮�濮嬬櫥褰曪紝浣跨敤URL鐩存帴杩涘叆鐧诲綍椤甸潰鐨�
    return render(request, 'login.html')

#    鐧诲嚭绯荤粺
def logout(request):
    request.session['is_login'] = '0'
    request.session['login_name'] = ''
    
    return redirect('login')

#    鑾峰彇鐧婚檰鐢ㄦ埛淇℃伅
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

#    鏄剧ず鎻愮ず淇℃伅鍒楄〃
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

#    绠＄悊鍛樻彁绀虹敤鎴锋敞鍐屾巿鏉�
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

#    绠＄悊鍛樻彁绀轰俊鎭垹闄�
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

#    鐢ㄦ埛涓汉棣栭〉
@check_login
def iframe_welcome(request):

#     candidate_obj = Candidate_resource.objects[0:5]
#     candidate_obj = Candidate_resource.objects(company='缇庡洟', name='鍛ㄧ拹')
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

#    绠＄悊鍛樼畝鍘嗙鐞�
def resume_manage(request):
    return render(request, 'talent_manage_html/resume_manage.html')

#    鑾峰彇绠�鍘嗚缁嗕俊鎭�
def get_resumeInfo(request):
    
    if request.method == "GET":
        telephone = request.GET.get('telephone')
    
    resume_obj = Candidate_resource.objects.filter(telephone=telephone).as_pymongo()
    resume_obj_dict = resume_obj[0]
    
#     if resume_obj_dict.get('birthday'):
#         birthday_string = user_obj_dict.get('birthday').date().isoformat()
#         user_obj_dict.update({'birthday':birthday_string})
#     
#     if user_obj_dict.get('enter_time'):
#         enter_time_string = user_obj_dict.get('enter_time').date().isoformat()
#         user_obj_dict.update({'enter_time':enter_time_string})
#     
#     if user_obj_dict.get('create_time'):
#         create_time_string = user_obj_dict.get('create_time').date().isoformat()
#         user_obj_dict.update({'create_time':create_time_string})
#     
#     if user_obj_dict.get('dimission_time'):
#         create_time_string = user_obj_dict.get('dimission_time').date().isoformat()
#         user_obj_dict.update({'dimission_time':create_time_string})
    
    return render(request, 'talent_manage_html/show_resume_info.html', resume_obj_dict)

#    绠�鍘嗗娉ㄦ坊鍔�
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
        
        print(filter_params_dict)
        print(update_params_dict)
        
        #    鏃堕棿鎴�
        date_strf = time.time()
        #    鏍煎紡鍖栨椂闂�
        format_time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        #    鏈�杩戠殑鎿嶄綔鑰�
        last_operator_login_name = request.session.get('login_name')
    
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

#    鏍规嵁妫�绱㈡潯浠讹紝缁熻鏁版嵁鏉℃暟
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
    
#     candidate_obj = Candidate_resource.objects(company='缇庡洟', name='鍛ㄧ拹')
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

#    妫�绱㈢畝鍘�
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
#         # candidate_obj = CandidateResource.objects.filter(company='缇庡洟', name='鍛ㄧ拹').values('name', 'telephone', 'company')[:10]
#         # candidate_obj = CandidateResource.objects.filter(**filter_params_dict)[0:1]   #---    杩欑鏂瑰紡鎶ラ敊
#         candidate_obj = CandidateResource.objects.filter(**filter_params_dict).values('name', 'telephone', 'company', 'position', 'new_remark')[from_search_count:from_search_count + 10]
#     else:
#         candidate_obj = CandidateResource.objects.all().values('name', 'telephone', 'company', 'position', 'new_remark')[from_search_count:from_search_count + 10]

    collection_obj = Candidate_resource.objects(**filter_params_dict)[0:1]
    candidate_obj = collection_obj._collection_obj.find(collection_obj._query)[from_search_count:from_search_count + 10]
    
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

#    娣诲姞绠�鍘�
def insert_jianli(request):
    filter_params_dict = {}
    update_params_dict = {}

    for key, value in request.GET.items():
        if key == 'telephone':
            value = int(value)
            print(type(value))
            filter_params_dict.update({key: value})
        else:
            if value:
                # print(key + ':' + value)
                update_params_dict.update({key: value})
            else:
                update_params_dict.update({key: ''})

#     conment = update_params_dict['new_remark']
    conment = update_params_dict.pop('new_remark')
    print(conment)
    
    print(filter_params_dict)
    print(update_params_dict)
    
    #    鏃堕棿鎴�
    date_strf = time.time()
    #    鏍煎紡鍖栨椂闂�
    format_time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    status = 'error'
    if filter_params_dict:
        if(conment != ''):
            one_remark = One_remark(comment=conment, date_strf=date_strf, date_string=format_time_string)
            candidate_obj = Candidate_resource.objects(**filter_params_dict).update(upsert= True, **update_params_dict, push__new_remark=one_remark)
            if candidate_obj:
                status = 'success'
        else:
            candidate_obj = Candidate_resource.objects(**filter_params_dict).update(upsert= True, **update_params_dict)
            if candidate_obj:
                status = 'success'

    return JsonResponse({'status': status})

#-----------------------------------------------------------------------------------------------------------------------

#    鏇存柊绠�鍘�
def update_jianli(request):
    filter_params_dict = {}
    update_params_dict = {}

    for key, value in request.GET.items():
        if key == 'telephone':
            value = int(value)
            print(type(value))
            filter_params_dict.update({key: value})
        else:
            if value:
                # print(key + ':' + value)
                update_params_dict.update({key: value})
            else:
                update_params_dict.update({key: ''})

#     conment = update_params_dict['new_remark']
    conment = update_params_dict.pop('new_remark')
    print(conment)
    
    print(filter_params_dict)
    print(update_params_dict)
    
    #    鏃堕棿鎴�
    date_strf = time.time()
    #    鏍煎紡鍖栨椂闂�
    format_time_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    status = 'error'
    if filter_params_dict:
#         candidate_obj = CandidateResource.objects.filter(**filter_params_dict).update(**update_params_dict)
        
#         candidate_resource.update(filter_params_dict, {"$set":update_params_dict,
#                                                     "$push":{"new_remark":{
#                                                                                    "comment" : "1101鏇存柊鏁版嵁鍜屾洿鏂板唴宓屾枃妗ｉ兘宸茬粡濂界敤浜�",
#                                                                                    "date_strf":date_strf,
#                                                                                    "date_string":format_time_string
#                                                                                    }}})
        
        if(conment != ''):
            one_remark = One_remark(comment=conment, date_strf=date_strf, date_string=format_time_string)
#             candidate_obj = Candidate_resource.objects(**filter_params_dict).update(push__new_remark=one_remark)
            candidate_obj = Candidate_resource.objects(**filter_params_dict).update(upsert= True, **update_params_dict, push__new_remark=one_remark)
            if candidate_obj:
                status = 'success'
        

    return JsonResponse({'status': status})
#-----------------------------------------------------------------------------------------------------------------------

#    绠＄悊鍛樻潈闄愭樉绀�
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

#    绠＄悊鍛樻潈闄愭坊鍔�
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

#    绠＄悊鍛樻潈闄愬垹闄�
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

#    鏄剧ず绠＄悊鍛樿鑹插垪琛�
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

#    绠＄悊鍛樿鑹叉坊鍔�
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

#    绠＄悊鍛樿鑹插垹闄�
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

#    鏄剧ず鐢ㄦ埛鍒楄〃
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

#    鐢ㄦ埛璐﹀彿寮�鍏�
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

#    鍒犻櫎鐢ㄦ埛
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

#------------------------------------------
# 
# from .forms import UserForm
# from .views_mongo import import_one_resume
# from lmk_app_backup.lmk_tools.resume_tools.read_file_word import read_word
# #    绠�鍘嗗鍏�
# def resume_import(request):
#     login_name = request.session.get('login_name')
#     
#     if request.method == 'POST':
#         userform = UserForm(request.POST, request.FILES)
#         
#         resume_file = request.FILES.get("upload", None)    # 鑾峰彇涓婁紶鐨勬枃浠讹紝濡傛灉娌℃湁鏂囦欢锛屽垯榛樿涓篘one
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

def company_list(request):
#     return render(request, 'admin_html/admin-role-add.html')
    return render(request, 'client_html/company_html/company_list.html')
def company_list_add():
    return render(request)




