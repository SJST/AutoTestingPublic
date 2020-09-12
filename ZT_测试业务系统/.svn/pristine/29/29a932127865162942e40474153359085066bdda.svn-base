# csv 导入MongoDB 命令
# 参数说明：
# d:数据库名
# c:collection名
# type:文件类型，指明是csv文件
# headline:指明第一行是列名，不需要导入
# file:csv文件路径及名字
# 更多参数请执行 mongoimport --help查看
# mongoimport -d test -c candidate_resource --type csv --headerline --file D:\CESC-ftp_server\jianliku_app\workspace\jianliku_test\files\candidate_resource_20181018.csv

# 打印mongo查询语句
# print queryset._query
# queryset.explain()

#---                            MongoDB 常用查询语句
#	$regex 是个修饰符 跟$set一样
#	正则表达式
#	.pretty()增加数据可读性
# db.candidate_resource.find({"name":{$regex:"王为冬"}}).pretty()

#	,{multi:true}更新多条数据 等同updateMany()
# db.candidate_resource.update({"name":{$regex:"王为冬"}},{$set:{"update_time":""}},{multi:true})

#	$rename 是个修饰符 跟$set一样
#	更改字段名称
# db.candidate_resource.update({"name":{$regex:"王为冬"}},{ $rename: { "update_time": "lastModified" }},{multi:true})

#	格林威治时间
# db.candidate_resource.update({"name":{$regex:"王为冬"}},{$set:{"lastModified":new Date()}},{multi:true})

#	时间转换成字符串存储
# db.candidate_resource.update({"name":{$regex:"王为冬"}},{$set:{"lastModified":new Date().toLocaleString()}},{multi:true})

#	$currentDate 是个修饰符 跟$set一样
#	"lastModified": { $type: "date" }
# db.candidate_resource.update(
#    {"name":{$regex:"王为冬"}},
#    {
#      $currentDate: {
#         lastModified: true,
#         "lastModified": { $type: "timestamp" }
#      },
#      $set: {
#         "email": "309061381@qq.com",
#         "education": "本科"
#      }
#    },
#    {multi:true}
# )

#	通过js输出信息
# db.candidate_resource.find({"new_remark":{$type:2}}).forEach( function(one_info) { print( "new_remark: " + one_info.new_remark ); } );

#	更改字段类型为Array类型
# db.candidate_resource.find({"new_remark":{$type:2}}).forEach( function(one_info) { 
#     //print( "new_remark: " + typeof(one_info.new_remark) ); 
#     one_info.new_remark = Array({new Date().toLocaleString():one_info.new_remark});
#     //print( "new_remark: " + typeof(one_info.new_remark) ); 
#     //print( "new_remark: " + one_info.new_remark[0]); 
#     
#     db.candidate_resource.save(one_info)
# } );

#	显示ISODate()类型的时间戳
# ISODate().valueOf()

#	清洗备注
# db.candidate_resource.find({"name":{$regex:"王为冬"}}).forEach( function(one_info) { 
#     tmp_remark = [{"before":one_info.new_remark[0]}]
#     one_info.new_remark = tmp_remark;
#     //one_info.new_remark = ["王为冬"];
#     db.candidate_resource.save(one_info)
# } );
# db.candidate_resource.find({"name":{$regex:"王为冬"}}).pretty()

#	更改内嵌文档的键名，不能对数组内的内嵌文档的键名进行修改
# db.candidate_resource.update({"name":{$regex:"王为冬"}},{ $rename: { "new_remark.before": "new_remark.now" }},{multi:true})

#-----------	例子	------------
# db.candidate_resource.update(
#     {"telephone" : NumberLong("15909850681")},
#     {$unset:{"new_remark.0.name":""}}
# )
# db.candidate_resource.update(
#     {"telephone" : NumberLong("15909850681")},
#     {$set:{"new_remark.0.name":"王为冬"}}
# )
# db.candidate_resource.find({"telephone" : NumberLong("15909850681")}).pretty()
#-----------	例子	------------





