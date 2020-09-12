# from django.db import models
# from django.contrib import admin

from mongoengine import *
from datetime import datetime
from bson.json_util import default
#from pip._vendor.pkg_resources import require
# from mongoengine import connect
# from mongoengine import Document
# from mongoengine import StringField
connect('LMK_DB')

class One_remark(EmbeddedDocument):
    comment = StringField()
#     date = DateTimeField(default=datetime.datetime.now(), required=True)
    date_strf = FloatField(default=datetime.now(), required=True)
#     date = ComplexDateTimeField(default=datetime.datetime.utcnow, required=True)
    date_string = StringField()
    
    last_operator = StringField()
    del_flag = IntField(default=0)  #    删除，只做标记变更，不做真实删除
    
class One_prompt(EmbeddedDocument):
    login_name = StringField()
    register_real_name = StringField()
    comment = StringField(default=" 请求开通账号！")
    date_strf = FloatField(default=datetime.now(), required=True)
    date_string = StringField()
    
    read_status = IntField(default=0)
    del_flag = IntField(default=0)
    
class Candidate_resource(Document):
    _id = ObjectIdField()
    name = StringField(required=True)
    telephone = IntField(required=True, unique=True)
    district_city = StringField()
    province_city = StringField()
    industry_influence = StringField()
    company = StringField()
    position = StringField()
    education = StringField()
    property_direction = StringField()
    work_experience = StringField()
    project_experience = StringField()
    email = EmailField()
    age = StringField()
    gender = StringField()
    address = StringField()
    skills = StringField()
    work_ability = StringField()
    language_ability = StringField()
    certificate = StringField()
    career_intention = StringField()
    self_evaluation = StringField()
    domains = StringField()
    companycity = StringField()
    companyaddress = StringField()
    personal_profile = StringField()
    extra_info = StringField()
    hobby_info = StringField()
    new_remark = ListField(EmbeddedDocumentField(One_remark), required=True)
    
    last_operator = StringField()
    update_time = DateTimeField(Default=datetime.now())
    del_flag = IntField(default=0)
#     new_remark = ListField(StringField(max_length=30), required=True)
    
class Candidate_user(Document):
    _id = ObjectIdField()
    login_name = StringField(required=True, unique=True)    #    昵称，用于登陆系统的账号
    password = StringField(required=True)
    real_name = StringField(required=True)  #    真实姓名
    
    birthday = DateTimeField()
    telephone = IntField(required=True)
    
    gender = StringField()
    address = StringField() #    家庭住址
    email = EmailField()
    marital_status = StringField()  #    是否已婚
    remark = ListField(EmbeddedDocumentField(One_remark))  #    备注，表现如何，是否准备加薪，应等同于简历管理的备注功能
    enter_time = DateTimeField()    #    入职时间
    dimission_time = DateTimeField()    #    离职时间
    rank = StringField()    #    职级，是否是合伙人，TL等
    work_status = BooleanField(default=True) #    工作状态，是否在职
    account_status = BooleanField(default=False)    #    账号状态，是否启用
    
    role_name = StringField()   #    角色名称，
    permission_name = ListField() #    权限名称，应该是list，其中可以有多种权限
    
    create_time = DateTimeField(Default=datetime.now()) #    用户创建时间
    
    #    最后操作信息要改成list，list中是修改时间和修改者的键值对
    update_time = DateTimeField(Default=datetime.now())
    last_operator = StringField()
    
    #    管理员提示信息，其他角色暂时没有提示信息功能
    prompt_message = ListField(EmbeddedDocumentField(One_prompt))   #    可以用 EmbeddedDocumentListField
    
    del_flag = IntField(default=0)  #    删除用户，只做标记变更，不做真实删除

class Skin_color(Document):
    _id = ObjectIdField(required=True)
    color_code = StringField(required=True, unique=True)
    color_name = StringField(required=True)
    
#     meta = {'collection': 'skin_color'}

STATUS = (
            {0:"unavailable"},
            {1:"available"}
        )

class Permission(Document):
    _id = ObjectIdField()
    permission_name = StringField(required=True)
    permission_description = StringField(required=True)
    create_time = DateTimeField(default=datetime.now(), required=True)
    update_time = DateTimeField(default=datetime.now(), required=True)
    last_operator = StringField(default="CESC")
    available_status = StringField(choices=STATUS)

class Role(Document):
    _id = ObjectIdField()
    role_level = IntField(default=10)
    role_name = StringField(required=True, unique=True)
    role_description = StringField(required=True)
    create_time = DateTimeField(default=datetime.now(), required=True)
    update_time = DateTimeField(default=datetime.now(), required=True)
    last_operator = StringField(default="CESC")
    available_status = StringField(choices=STATUS)
    #下面是客户公司的model
class Interview_information(EmbeddedDocument):
    position_info= StringField(require=True)
    Referral_Info= StringField(require=True)
    interview_times= IntField(require=True)
    offer_times = IntField(require =True)
class client_company(Document):
    company_name =StringField(require=True)
    company_industry =StringField(require=True)
    company_city = StringField(require=True)
    company_contacts = StringField(require=True)
    contacts_telephone = IntField(require=True)
    contacts_class = StringField(require=True)
    interview_information=  ListField(EmbeddedDocumentField(Interview_information), required=True)

# Create your models here.
# class CandidateResource(models.Model):
#     name = models.CharField(max_length=32)
#     telephone = models.CharField(primary_key=True, max_length=11)
#     district_city = models.CharField(blank=True, null=True, max_length=100)
#     province_city = models.CharField(blank=True, null=True, max_length=100)
#     industry_influence = models.CharField(blank=True, null=True, max_length=100)
#     company = models.CharField(blank=True, null=True, max_length=100)
#     position = models.CharField(blank=True, null=True, max_length=100)
#     education = models.CharField(blank=True, null=True, max_length=100)
#     property_direction = models.CharField(blank=True, null=True, max_length=100)
#     work_experience = models.CharField(blank=True, null=True, max_length=100)
#     email = models.CharField(blank=True, null=True, max_length=100)
#     address = models.CharField(blank=True, null=True, max_length=100)
#     skills = models.CharField(blank=True, null=True, max_length=100)
#     domains = models.CharField(blank=True, null=True, max_length=100)
#     companycity = models.CharField(blank=True, null=True, max_length=100)
#     companyaddress = models.CharField(blank=True, null=True, max_length=100)
#     new_remark = models.CharField(db_column='new_remark', blank=True, null=True, max_length=200)
# 
#     class Meta:
#         managed = True
#         db_table = 'candidate_resource'

# class CandidateUser(models.Model):
#     username = models.CharField(max_length=32)
#     password = models.CharField(max_length=32)
#     realname = models.CharField(max_length=32)
# 
#     class Meta:
#         managed = True
#         db_table = 'candidate_user'



    
# admin.site.register(CandidateResource)
# admin.site.register(CandidateUser)
# admin.site.register(TestUser)
# admin.site.register(MongoUser) #---
