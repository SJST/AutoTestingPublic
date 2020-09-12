//点击编辑按钮td可编辑
var ID_list=[];
$("#tbody_result").on("click", "a[title='编辑']", function(){
			var goal_td=$(this).parent('td');
			var goal_tr=$(goal_td).parent('tr');
			goal_tr.children('td').each(function(j){
				if (j<5){
				$(this).attr('contenteditable',"true");
				}
			});				
});
//li 点击变颜色 和search-div定位 隐藏显示 
//公司 
$("#company").click(function(){
	$(this).css("background-color", "#ff5000");
	$(this).css("color", "#fff");
	$("#indu").css("background-color", "#fff");
	$("#indu").css("color", "#f40");
	$("#city").css("background-color", "#fff");
	$("#city").css("color", "#f40");
	$("#class").css("background-color", "#fff");
	$("#class").css("color", "#f40");
	$(".search-company").css("display","block")
	$(".search-industy").css("display","none")
	$(".search-city").css("display","none")
	$(".search-class").css("display","none")
	
});
//行业
$("#indu").click(function(){
	$("#company").css("background-color", "#fff");
	$("#company").css("color", "#f40");
	$("#city").css("background-color", "#fff");
	$("#city").css("color", "#f40");
	$("#class").css("background-color", "#fff");
	$("#class").css("color", "#f40");
	$(this).css("background-color", "#ff5000");
	$(this).css("color", "#fff");
	$(".search-company").css("display","none")
	$(".search-city").css("display","none")
	$(".search-class").css("display","none")
	$(".search-industy").css("display","block")
	$(".search-industy").css("margin-top","4px")
});
//城市
$("#city").click(function(){
	$("#company").css("background-color", "#fff");
	$("#company").css("color", "#f40");
	$("#indu").css("background-color", "#fff");
	$("#indu").css("color", "#f40");
	$("#class").css("background-color", "#fff");
	$("#class").css("color", "#f40");
	$(this).css("background-color", "#ff5000");
	$(this).css("color", "#fff");
	$(".search-company").css("display","none")
	$(".search-industy").css("display","none")
	$(".search-city").css("display","block")
	$(".search-class").css("display","none")
	$(".search-city").css("margin-top","4px")
});
//类型
$("#class").click(function(){
	$("#company").css("background-color", "#fff");
	$("#company").css("color", "#f40");
	$("#indu").css("background-color", "#fff");
	$("#indu").css("color", "#f40");
	$("#city").css("background-color", "#fff");
	$("#city").css("color", "#f40");
	$(this).css("background-color", "#ff5000");
	$(this).css("color", "#fff");
	$(".search-company").css("display","none")
	$(".search-industy").css("display","none")
	$(".search-city").css("display","none")
	$(".search-class").css("display","block")
	$(".search-class").css("margin-top","4px")
});

$(document).ready(function(){
$('#table_head').hide();
//$.fn.editable.defaults.mode = 'inline';
$("#tbody_result").on("click", "td#company_name a", function(){
	var company_name= $(this).text()
	
	Hui_admin_tab(this);
});

var test_num=0

$.ajax({
	async: false,
	url:"company-ajax",
	type:'GET',
	dataType: 'json',
	data:{'test_num':test_num},
	success:function(ret){
		
		$('#table_head tr:gt(0)').remove();
		$('#table_head').show();
		var company_list=[];
		var industy_list=[];
		var city_list=[];
		var client_list=[];
		$.each(ret, function(i,item){
			if(ID_list.indexOf(item.company_class)==-1){
				ID_list.push(item.ID)
			}
			if(client_list.indexOf(item.company_class)==-1){
				client_list.push(item.company_class)
			}
			if(company_list.indexOf(item.company_name)==-1){
				company_list.push(item.company_name)
			}
			if(industy_list.indexOf(item.industry)==-1){
				industy_list.push(item.industry)
			}
			if(city_list.indexOf(item.city_list)==-1){
				city_list.push(item.company_address)
			}
			var company_name=item.company_name;
        	var url ="{% url 'company-info' %}?company_name="+company_name;
			var tr_new=$('<tr class="order" border="3"></tr>');
			
			//获得 小对象个数用于table合并
			
			tr_new.append(
					'<td height="20px" width="100px"class="big_table" id="company_name">'+'<a data-title="公司信息" data-href="' + url + '" class="c-primary" href="javascript:;">'+item.company_name + '</a>' +'</td>'+
					'<td height="20px" width="100px"class="big_table" >' + item.company_address+ '</td>'+
					'<td height="20px" width="100px" class="big_table" id="position_num">'+item.position_num+'</td>'+
					'<td height="20px" width="100px"class="big_table" >' + item.stage + '</td>'+
					'<td height="20px" width="100px"class="big_table" >' + item.company_class + '</td>'+
					'<td height="20px" width="100px"class="big_table" >' +'<a title="编辑" href="javascript:;" class="ml-5" style="text-decoration:none"><i class="Hui-iconfont">&#xe6df;</i></a>' +
																		  '<a title="保存" href="javascript:;" class="ml-5" style="text-decoration:none"><i class="Hui-iconfont">&#xe6a7;</i></a>'+
																		  '<a title="删除" href="javascript:;" style="text-decoration:none"><i class="Hui-iconfont">&#xe6e2;</i></a>'+'</td>'
					);
			$("#tbody_result").append(tr_new);

		});
		//公司搜索下拉
		$(function(){
			$( "#search_company" ).autocomplete({
			      source: company_list,
			      messages:{
			          noResults:function(){
			        	 // layer.msg('没有与该关键字匹配的公司！',{icon:2,time:1000}  
			        	 // );
			          },
			          results:function(){  
			          }}
			    });
		});
		//行业
		$(function(){
			$( "#search_industy" ).autocomplete({
			      source: industy_list,
			      messages:{
			          noResults:function(){
			        	
			          },
			          results:function(){  
			          }}
			    });
		});
		//城市
		$(function(){
			$( "#search_city" ).autocomplete({
			      source: city_list,
			      messages:{
			          noResults:function(){
			        	
			          },
			          results:function(){  
			          }}
			    });
		});
		//类型
		$(function(){
			$( "#search_class" ).autocomplete({
			      source: client_list,
			      messages:{
			          noResults:function(){
			        	
			          },
			          results:function(){  
			          }}
			    });
		});
	 }
});
//保存操作
$("#tbody_result").on("click", "a[title='保存']", function(){
	var dic=[]
	var p_td=$(this).parent('td');
	var idx = $(this).closest('tr').index()
	var p_tr=$(p_td).parent('tr');
	p_tr.children('td').each(function(j){
		ID=ID_list[idx]
		if(dic.indexOf(ID)==-1){
			dic.push({"ID":ID})
		}
			
		if (j==0){
		var company_name=$(this).text();
		dic.push({"company_name":company_name})
		}
		if (j==1){
			var company_address=$(this).text();
			dic.push({"company_address":company_address})
			}
		if (j==2){
			var position_num=$(this).text();
			dic.push({"position_num":position_num})
			}
		if (j==3){
			var stage=$(this).text();
			dic.push({"stage":stage})
			}
		if (j==4){
			var company_class=$(this).text();
			dic.push({"company_class":company_class})
			}
	});
	layer.confirm('确定要修改么？',{
		  btn: ['确定','取消'] //按钮
	},function(){{inco:1}
		$.ajax({
	    	async: false,
	      	url:"list_exid",
	    	type:'POST',
	    	dataType: 'json',
	    	data:{"dic":dic},
	    	success:function(ret){
	    		
	    		$.each(ret, function(i,item){
	    			
	    			if(item=='success'){
	    				layer.confirm('已修改!',{
	    					  btn: ['确定','取消'] //按钮 
	    				},function(){{inco:1}
	    				window.location.reload();
	    		    	  });	
	            	}else{
	            		alert("添加失败");
	            	}
	    		});
	    	},
	    	error:function(ret){
	    	  	alert("1111");
	      	}
		});
		
	});
});
//删除操作
$("#tbody_result").on("click", "a[title='删除']", function(){
	var del_company_name = $(this).parents("tr").find("#company_name").text();
	
	layer.confirm('确定要删除么？',{
		  btn: ['确定','取消'] //按钮
	},function(){{inco:1}
		$.ajax({
			type: 'POST',
			url:"list_del",
			data: {'company_name':del_company_name}	,
			success: function(ret){
					$.each(ret, function(i,item){
		    			if(item=='success'){
		    				layer.confirm('已删除',{
		    					  btn: ['确定','取消'] //按钮 
		    				},function(){{inco:1}
		    				window.location.reload();
		    		    	  })
		            	}else{
		            		alert("添加失败");
		            }
		    				
		    	});
			}
		});
	});
	
});	

var index=document.getElementsByTagName("td").length;
if (index==0){
	$('#table_head').hide();
	
}
});
$('.search_button').click(function(){
	var search_text="";
	var search_company = $('#search_company').val();
	var search_industy = $('#search_industy').val();
	var search_city = $('#search_city').val();
	var search_class = $('#search_class').val();
	if (search_company!=""){
		search_text="search_company"+":"+search_company
	}
	if (search_industy!=""){
		search_text="search_industy"+":"+search_industy
	}
	if (search_city!=""){
		search_text="search_city"+":"+search_city
	}
	if (search_class!=""){
		search_text="search_class"+":"+search_class
	}
	//alert(search_text);
	if (search_text!=""){
		$.ajax({
	    	async: false,
	      	url:"search_ajax",
	    	type:'POST',
	    	dataType: 'json',
	    	data:{"search_text":search_text},
	    	success:function(ret){
	    		if(ret!=""){
		    		var reset_div=$("#reset")
		    		reset_div.empty().append('<button type="button" class="btn btn-default " id="reset_button">'+"重置"+ '</button>')
		    		$('#table_head tr:gt(0)').remove();
		    		$.each(ret, function(i,item){
		    			var tr=$('<tr></tr>');
		    			
		    			//获得 小对象个数用于table合并
		    			
		    			tr.append(
		    					'<td height="20px" width="100px"class="big_table" id="company_name">'+item.company_name +'</td>'+
		    					'<td height="20px" width="100px"class="big_table" >' + item.company_address+ '</td>'+
		    					'<td height="20px" width="100px" class="big_table" id="position_num">'+item.position_num+'</td>'+
		    					'<td height="20px" width="100px"class="big_table" >' + item.stage + '</td>'+
		    					'<td height="20px" width="100px"class="big_table" >' + item.company_class + '</td>'+
		    					'<td height="20px" width="100px"class="big_table" >' +'<a title="编辑" href="javascript:;" class="ml-5" style="text-decoration:none"><i class="Hui-iconfont">&#xe6df;</i></a>' +
		    																		  '<a title="保存" href="javascript:;" class="ml-5" style="text-decoration:none"><i class="Hui-iconfont">&#xe6a7;</i></a>'+
		    																		  '<a title="删除" href="javascript:;" style="text-decoration:none"><i class="Hui-iconfont">&#xe6e2;</i></a>'+'</td>'
		    					);
		    			$("#tbody_result").append(tr);
	
		    		});
	    		//window.location.reload();
	    	   }
	    	   else{
	    		   layer.msg('搜索结果不存在！',{icon:2,time:1000}  
	    	    	  );
	    		}
	    	}
		});
	}
	else{
		   layer.msg('搜索内容不能为空！',{icon:2,time:1000}  
    	  );
	}
//	var tmall_store = $('#tmall_store').val();
	//alert(tmall_store);
	$("#reset_button").click(function(){
		window.location.reload();
	});
});
function xieyi(){
	$("#company").trigger("click");
	};
	$(document).ready(function(){
	       
	     window.onload=xieyi;
	    });