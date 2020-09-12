from django.shortcuts import render, HttpResponse
from .models import Candidate_user
from bson.json_util import dumps
from django.core.paginator import Paginator


import json

def check_exist(request):
    login_name = request.GET.get('login_name')
    candidate_user = Candidate_user.objects.filter(login_name=login_name)
    
    status = 0
    
    if candidate_user:
        status = 1
    
    data_json = {"status":status, "login_name":login_name}
    
    json_str = json.dumps(data_json)
    print(json_str)
    return HttpResponse(json_str)

def register(request):
    login_name = request.GET.get('login_name')
    real_name = request.GET.get('real_name')
    print(login_name + '-' + real_name)
    
    candidate_user = Candidate_user.objects.filter(login_name=login_name)
    
    if candidate_user:
        return render(request, 'register_failed.html')
    else:
        return render(request, 'register_success.html')
    
    

def index(request):  
#     entry = CandidateModel(name='于姗姗')  
#     entry.save()  
#     resp = "hello %s" %(entry.name)
#     
#     obj = CandidateModel.objects.all()
#     print(obj[0].name)
    
    return render(request, 'index.html')
    
def change_name(request):
    
    username = request.GET['username']
    print(username)
    data_json = {'user':username + ' is ' +'CESC'}
    print(data_json)
    json_str = json.dumps(data_json)
    
    
    return HttpResponse(json_str)
    
def show_data(request):
    
    page_num = request.GET['page_num']
    print(page_num)
    
    query_set = Candidate_user.objects.all()
    candidate_obj = query_set._collection_obj.find(query_set._query)[0:10]
    print(type(query_set._cursor))
    tmp_list = query_set._cursor_obj
    print(tmp_list)
    data_json = dumps(tmp_list, ensure_ascii=False)
    print(data_json)
    
    
    
    paginator = Paginator(candidate_obj, 10)
    one_page_list = paginator.object_list
    
    print(one_page_list)
    print(type(one_page_list))
    
    data_json = dumps(one_page_list, ensure_ascii=False)
#     data_json = serializers.serialize('json', candidate_obj, ensure_ascii=False)
    print(data_json)
    return HttpResponse(data_json)
    
    
    
    
      