#    这个是数据仓库配置的views
# from lmk_app.models import Candidate_resource
import os
import sys
import importlib
importlib.reload(sys)

from lmk_app.models import Candidate_user,InitializationData,SwaggerAddressData,\
    SwaggerData
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

#    展示数据仓库配置页面
def db_house_config(request):
    user_obj = InitializationData.objects.order_by('-ID').as_pymongo()
    
    result_json = dumps(user_obj, ensure_ascii=False)
    print(result_json)
    
    result_count = user_obj.count()
    result_dict = {
        'result_count':result_count,
        'result_json':result_json
    }
    return render(request,'db_house_html/db_house_config.html',result_dict)

#    点击swagger展示页面
def swagger_chick_show(request):
    if request.method == "GET":
        ID = request.GET.get('ID')
    user_obj = SwaggerAddressData.objects.filter(ID=ID).as_pymongo()
    result_json = dumps(user_obj, ensure_ascii=False)
    print(result_json)
    result = {
        "data":result_json
        }
    
   
    return render (request, 'db_house_html/get_swagger_info.html', result)


#     点击查看DB用户名密码
def DB_chick_show(request):
    if request.method == "GET":
        ID = request.GET.get('ID')
    
    user_obj = InitializationData.objects.filter(ID=ID).as_pymongo()
    user_obj_dict = user_obj[0]
    DB_info = {}
    DB_info['DB_mark'] = user_obj_dict.get("DBMark")
    DB_info['DB_password'] = user_obj_dict.get("DBPassword")
    return render (request, 'db_house_html/T3_01_get_DB_info.html', DB_info)


def db_house_index(request):
    user_obj = InitializationData.objects.order_by('-ID').as_pymongo()
    
    result_json = dumps(user_obj, ensure_ascii=False)
   
    
    result_count = user_obj.count()
    result_dict = {
        'result_count':result_count,
        'result_json':result_json
    }
    return render (request, 'db_house_html/T3_02_db_house_switch/db_house_index.html',result_dict)
def controller(request):
    result = []
    server_name = request.GET.get('server')
    print(server_name)
    YxData = SwaggerData.objects.all().as_pymongo()
    for item in YxData:
        DB_server = item.get('server')
        if DB_server == server_name:
            if item.get('controller'):
                if item.get('controller') not in result:
                    result.append(item.get('controller'))
    result.append('其他')
    return JsonResponse({'data':result})
                     
def API(request):
    result = []
    controller_name = request.GET.get('controller')
    YxData = SwaggerData.objects.all().as_pymongo()
    for item in YxData:
        DB_controller = item.get('controller')
        if DB_controller == controller_name:
            if item.get('api'):
                if item.get('api') not in result:
                    result.append(item.get('api'))
    result.append('其他')
    return JsonResponse({'data':result})           
      