# from django.db import models
# from django.contrib import admin

import time
from mongoengine import *
from datetime import datetime
from bson.json_util import default
from pip._vendor.pkg_resources import require
from msilib.schema import Class
#from pip._vendor.requests.api import post
# from mongoengine import connect
# from mongoengine import Document
# from mongoengine import StringField
connect("LMK_DB")

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
    name = StringField(required=True)   #    姓名
    telephone = IntField(required=True, unique=True)    #    电话
    email = EmailField()    #    邮箱
    gender = StringField()  #    性别
    age = StringField() #    年龄
    education = StringField()   #    教育
    company = StringField() #    公司
    position = StringField()    #    职位
    companycity = StringField() #    公司所在城市
    work_experience = StringField() #    工作经历
    project_experience = StringField()  #    项目经历
    extra_info = StringField()  #    额外信息
    
#     domains = StringField() #    领域
#     industry_influence = StringField()  #    行业影响力
#     province_city = StringField()   #    省市
#     district_city = StringField()   #    地区城市
#     address = StringField() #    住址
#     companyaddress = StringField()  #    公司所在地址
#     property_direction = StringField()  #    业务方向
#     career_intention = StringField()    #    职业意向
#     work_ability = StringField()    #    工作能力
#     skills = StringField()  #    技能
#     language_ability = StringField()    #    语言能力
#     certificate = StringField() #    证书
#     personal_profile = StringField()    #    个人简介
#     self_evaluation = StringField() #    自我评价
#     hobby_info = StringField()  #    兴趣爱好
    
#     new_remark = ListField(EmbeddedDocumentField(One_remark), required=True)
    new_remark = ListField(EmbeddedDocumentField(One_remark))   #    备注
    
    first_uploader = StringField()  #    第一位上传简历者
    first_upload_time = StringField()   #    第一次上传简历时间
    last_operator = StringField()   #    最后操作者
    update_time = StringField() #    最后更新的时间
    
    del_flag = IntField(default=0)  #    删除标识，假删除，删除标识为1
    new_import_flag = IntField()    #    新导入标识，新导入标识为1，初次导入之后，标识更新为0
#     new_remark = ListField(StringField(max_length=30), required=True)

    def __get_field_name__(self):
        return self.name
    
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
    team = StringField() # 所属团队
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
    
    
    #################################################
# class Interview_information(EmbeddedDocument):
#     position_info= StringField(require=True)#职位
#     Referral_Info= StringField(require=True)#推荐
#     interview_times= IntField(require=True)#面试次数
#     offer_times = IntField(require =True)#offer次数
# class client_company(Document):
#     company_name =StringField(require=True)
#     company_industry =StringField(require=True)
#     company_city = StringField(require=True)
#     company_contacts = StringField(require=True)
#     contacts_telephone = IntField(require=True)
#     contacts_class = StringField(require=True)
#     interview_information=  ListField(EmbeddedDocumentField(Interview_information), required=True)

# class new_contect(EmbeddedDocument):#新的联系人 
#     new_contectsName= StringField(require=True) #名字
#     new_contectsJob= StringField(require=True)#职务
#     new_contectsTel= IntField(require=True)#电话
#     new_contectsEmall= EmailField(require=True)
#     new_contectsLine= IntField(require=True)#座机
#     new_contectsOther= StringField(require=True)
#     new_contectsRemark= StringField(require=True)
 ######################客户展示和客户添加基本信息的model#######################################   

#     new_contects =  ListField(require=True)
##################################客户职位的model#############################
# 
#     Referral_Info= StringField(require=True)#推荐
#     interview_times= IntField(require=True)#面试次数
#     offer_times = IntField(require =True)#offer次数
class postition_info(Document):
    ID = IntField(require=True)#公司ID
    position_name = StringField(require=True)#职位信息
    company_name = StringField(require=True)#公司信息
    city_name = StringField(require=True)#城市信息 
    newstime = StringField(require=True) #发布时间 
    Referral_Info= StringField(require=True)#推荐
    interview_times= IntField(require=True)#面试次数
    offer_times = IntField(require =True)#offer次数
    #职能分类信息
    ############################################################################
    #    配置初始化数据存储类
class InitializationData(Document):
    ID = IntField(require=True)#    配置id
    Evn = StringField(require=True)#    环境名称
    Swagger = StringField(require=True)#    环境名称
    SwaggerAddress = ListField()  # Swagger地址
    SMD = StringField(require=True)# SMD地址
    DB  = StringField(require=True)
    DBPassword = StringField(require=True)
    DBMark = StringField(require=True)
    DemandAdress = StringField(require=True)
    DzdmCache = StringField(require=True)
    DzdmResponse = StringField(require=True)
    DzdmIP = StringField(require=True)
    del_flag = IntField(default=0)
    account_status = BooleanField(default=False)
    git = StringField(require=True)
    
# SwaggerAdressData
class SwaggerAddressData(Document):
    ID = IntField(require=True)#    标识id
    name = StringField(require=True)#    地址名称
    address = StringField(require=True)#    地址


class position_classification(Document):
    frist_level= StringField(require=True)
    second_level= StringField(require=True)
class position_info(Document):
    company_name = StringField(require=True)#公司名称
    position_name = StringField(require=True)#职位名称
    salary_range =  StringField(require=True)#薪资范围
    work_city = StringField(require=True)#工作城市
    position_class = StringField(require=True)#职能分类
    estimate_commission = StringField(require=True)#预计佣金
    Working_life = StringField(require=True)#工作年限
    Academic_requirements = StringField(require=True)#学历要求
    Age_requirements = StringField(require=True)#年龄要求
    gender = StringField(require=True)#性别要求
    work_duty = StringField(require=True)#工作职责
    qualifications = StringField(require=True)#任职资格
    ascription = StringField(require=True)#归属
    adviser = StringField(require=True)#顾问
    participant = StringField(require=True)#参与人
    department_info = StringField(require=True)#部门信息
    Interview_process = StringField(require=True)#面试流程
    Background = StringField(require=True)#背景
    Seeking_advice = StringField(require=True)#寻访建议
    other_info = StringField(require=True)#其他信息
    
    
class SingleValue(Document):
    '''
    单值代码 映射
    '''
    codetype = StringField(require=True),#单值代码 pid\
    code = StringField(),#码值\
    name = StringField(),#翻译值\
    mark = StringField(),#单值代码说明\
    class Meta:
        table_name ='T3-zt'
class SwaggerCommon(Document):
    '''
    swagger 服务信息
    '''
    server = StringField(require=True),#服务名称 pid\
    api = StringField(),#接口名称\
    method = StringField(),# 控制器\
    tags = StringField()
    description = StringField()
    summary = StringField()
    consumes = StringField()
    pid = StringField()
    ref = StringField()
    BeanDescription = StringField()
    ApiNum = IntField()
    Address = StringField()
class new_company(Document):
    '''
    测试沉淀表单
    
    '''
    ID=StringField(require=True,max_length=8)
    CD_name = StringField(require=True)#客户类别
    add_public = StringField()
    important_level = StringField()
    server=StringField()#公司性质
    controller = StringField()#行业
    api_change=StringField()
    jmx_address = StringField()#阶段
    brackground = StringField()
    content = StringField()#网站
    col_qpi = StringField()#网站
    method = StringField()#介绍
    other_info = StringField()
    flags=StringField()
    person = StringField()
    create_time = StringField(required=True)
    update_time = StringField(required=True)
    
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
