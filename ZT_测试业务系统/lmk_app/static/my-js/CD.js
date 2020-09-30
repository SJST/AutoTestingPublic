// 保存沉淀
$("#save-from").on('click',function(){
	// 定义一个元素  接收 指定 id 的元素
	var class_1=$("#class-1").val();
	var	class_2=$("#class-2").val();
	if (class_1!=""){
		company_class=class_1
	}
	else{
		company_class=class_2
		}
	var CD_name =$('#CD_name').val();
	var add_public = $('#add_public').val();
	var important_level = $('#11400001').val();
	var server = $('#server').val();
	var controller = $('#controller').val();
	var col_qpi = $('#col_qpi').val();
	var jmx_address = $('#jmx_address').val();
	var brackgound = $('#brackground').val();
	var content =  $('#content').val();
	var method = $('#method').val();
	var other_info = $('#other_info').val();
	var base_info = {'name':CD_name,
					'public':add_public,
					'important_level':important_level,
					'server':server,
					'controller':controller,
					'qpi':col_qpi,
					'address':jmx_address,
					'api_change':company_class
					};
	var Survey_info = {
			'brackground':brackgound,
			'content':content,
			'method':method,
			// 'company_highlights':company_highlights,
			// 'interview_process':interview_process,
			'other_info':other_info			
	};
	//传值
	// $.ajax({
	// 	async: false,
	// 	url:"/business_add",
	// 	type:'POST',
	// 	dataType: 'json',
	// 	data:{'base_info':base_info,'Survey_info':Survey_info/*'content_info':content_list*/},
	// 	success:function(ret){
	// 		$.each(ret, function(i,item){
	// 			if( item== 'success'){
	//         		var index = parent.layer.getFrameIndex(window.name);
	//         		layer.alert('添加成功!', {title:'添加成功', icon:1}, function(index){
	//         			parent.layer.close(index);	
	//         		});
	//         		location.reload();
	//         	}else{
	//         		alert("添加失败");
	//         	}
	// 		});
	// 	},
	//   	error:function(ret){
	// 	  	alert("1111");
	//   	}
	// });
});
//check 是否只能选择一个
$('#class-1').change(function(){
	var class_1=$("#class-1").val();
	alert(class_1);
	if (class_1!=""){
		$('#class-2').prop("checked",false);
	}else{
		$('#class-2').prop("checked",true);
	}
});
$('#class-2').change(function(){
	var class_2=$("#class-2").val();
	if (class_2!=""){
		$('#class-1').prop("checked",false);
	}else{
		$('#class-1').prop("checked",true);
	}
});

// //表单校验
// // $("#form-register").validate({
// // 	rules:{
// // 		CD_name:{
// // 			required:true,
// // 			minlength:4,
// // 			maxlength:30
// // 		}
// // 	},
// // 	 messages: {  
// // 	   CD_name: "请输入沉淀标题",
// // 	    maxlength: jQuery.validator.format("请输入一个长度最多是 {0} 的字符串"),  
// // 	    minlength: jQuery.validator.format("请输入一个长度最少是 {0} 的字符串")
// // 		},
// // 	onkeyup:false,
// // 	focusCleanup:true,
// // 	success:"valid",
// // 	submitHandler:function(form){
// // 		$(form).ajaxSubmit(ajax_option);
// // 	}
// //  });

// function xxx () {
// 	alert(11);
// 	$("#form-register").validate({
// 	 	rules: {
// 			CD_name: {
// 				required:true,
// 				minlength:4,
// 				maxlength:30
// 			}
// 		},
// 		messages: {
// 			CD_name: {
// 				required:"请输入沉淀标题",
// 				maxlength: jQuery.validator.format("请输入一个长度最多是 {0} 的字符串"),
// 				minlength: jQuery.validator.format("请输入一个长度最少是 {0} 的字符串")
// 			}
// 		},
// 		errorPlacement: function(error, element) {
// 			alert(111);
// 		}
		
// 		// focusCleanup:true,
// 		// success:"valid",
// 		// submitHandler:function(form){
// 		// 	$(form).ajaxSubmit(ajax_option);
// 		// }
// 	});
// }
 
//  $(function(){
// 	$("#save-from").on('click',function(){
// 		xxx();
// 	});
	
	
// });
