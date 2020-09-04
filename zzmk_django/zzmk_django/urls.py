"""zzmk_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# from django.conf.urls import *
# from django.conf.urls import include
from django.conf.urls import url
from lmk_app import views
from lmk_app import views2

urlpatterns = [
    path('admin/', admin.site.urls),
#     url(r'^$', views.index),
    
 
    url(r'^$', views.index, name='index'),
 
    url(r'^register-info$', views.register_info, name='register-info'),
   
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
  
    url(r'^get_userInfo/[^\/]*$', views.get_userInfo, name='get-userInfo'),
    
    url(r'^show-prompt-message/[^\/]*$', views.show_prompt_message, name='show-prompt-message'),
    url(r'^prompt-message-del', views.prompt_message_del, name='prompt-message-del'),
    url(r'^prompt-register-authorize', views.prompt_register_authorize, name='prompt-register-authorize'),

    url(r'^welcome', views.iframe_welcome, name='iframe-welcome'),

    url(r'^resume-manage', views.resume_manage, name='resume-manage'),
    url(r'^get-resumeInfo', views.get_resumeInfo, name='get-resumeInfo'),

    url(r'^search-jianli/[^\/]*$', views.search_jianli, name='search-jianli'),
    url(r'^insert-jianli/[^\/]*$', views.insert_jianli, name='insert-jianli'),
    url(r'^update-jianli/[^\/]*$', views.update_jianli, name='update-jianli'),
    url(r'^get-total-count/[^\/]*$', views.get_total_count, name='get-total-count'),

    url(r'^admin-permission$', views.admin_permission, name='admin-permission'),
    url(r'^admin-permission-add', views.admin_permission_add, name='admin-permission-add'),
    url(r'^admin-permission-del', views.admin_permission_del, name='admin-permission-del'),

    url(r'^admin-role$', views.admin_role, name='admin-role'),
    url(r'^admin-role-add$', views.admin_role_add, name='admin-role-add'),
    url(r'^admin-role-del', views.admin_role_del, name='admin-role-del'),

    url(r'^user-list$', views.show_user_list, name='show-user-list'),
    url(r'^user-account-switch', views.user_account_switch, name='user-account-switch'),
    url(r'^user-del', views.user_del, name='user-del'),
    url(r'^company-list$', views.company_list, name='company-list'),
    url(r'^company_add$', views.company_add, name='company-add'),
    url(r'^position_list$', views.position_list, name='position-list'),
    url(r'^position_add$', views.position_add, name='position-add'),
    #    数据仓库配置的url
    url(r'^db_house_config$', views2.db_house_config, name='db-house-config'),
    #    swagger地址展示地址
    url(r'^get_swagger_info$', views2.swagger_chick_show, name='get-swagger-info'),
    #    展示 DB用户名/密码
    url(r'^T3_01_get_DB_info', views2.DB_chick_show, name='get-DB-info'),
    #    db_house 操作列表页面
    url(r'^db_house_index', views2.db_house_index, name='db-house-index'),
    
    
    
]


