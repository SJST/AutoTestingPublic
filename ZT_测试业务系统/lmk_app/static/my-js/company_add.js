//这个公司添加模块的js

$("#save-from").on('click',function(){
	//生成base_info 和 Survey 的元素 
	var company_class;
	var class_1=$("#class-1").val();
	var	class_2=$("#class-2").val();
	if (class_1!=""){
		company_class=class_1
	}
	else{
		company_class=class_2
		}
	var company_name=$("#company_name").val();
	var company_size=$("#company_size").val();
	var company_nature=$("#company_nature").val();
	var industry=$("#industry").val();
	var stage=$("#stage").val();
	var company_address=$("#company_address").val();
	var company_website=$("#company_website").val();
	var company_introduction=$("#company_introduction").val();
	var packages=$("#package").val();
	var company_highlights=$("#company_highlights").val();
	var interview_process=$("#interview_process").val();
	var other_info=$("#other_info").val();
	var base_info = {'company_class':company_class,
					'company_name':company_name,
					'company_size':company_size,
					'company_nature':company_nature,
					'industry':industry,
					'stage':stage,
					'company_address':company_address
					};
	var Survey_info = {
			'company_website':company_website,
			'company_introduction':company_introduction,
			'package':packages,
			'company_highlights':company_highlights,
			'interview_process':interview_process,
			'other_info':other_info			
	};
	//传值 
	$.ajax({
    	async: false,
    	url:"{% url 'company-add' %}",
    	type:'POST',
    	dataType: 'json',
    	data:{'base_info':base_info,'Survey_info':Survey_info/*'content_info':content_list*/},
    	success:function(ret){
    		$.each(ret, function(i,item){
    			if( item== 'success'){
            		var index = parent.layer.getFrameIndex(window.name);
            		layer.alert('添加成功!', {title:'添加成功', icon:1}, function(index){
            			parent.layer.close(index);	
            		});
            		location.reload();
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