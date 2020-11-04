/*
	<body>
	    
	    <div class="paging"></div>
	
	    <script src="./index.js"></script>
	    <script>
	        let paging = new Paging({
	            total: 100,
	    </script>
	</body>
*/
/*  https://www.jq22.com/yanshi23441  */
function Paging(options) {
    let defaultValue = {
        total: 0,
        current: 1,
        firstText: '首页',
        prevText: '上一页',
        nextText: '下一页',
        lastText: '尾页',
        PageSize: 10,
        PageNum: 5,
        container: document.getElementsByClassName('paging')[0]
    }

    this.options = Object.assign({}, defaultValue, options);
    this.show();
    this.PageClick()
}

Paging.prototype.show = function () {
    let disable = "";
    let PageTotalNum = this.getPageTotalNum();
    this.options.container.innerHTML = "";
    if(this.options.current === 1){
        disable = 'disable'
    }
    this.createElement('first ' + disable, this.options.firstText);
    this.createElement('prev ' + disable, this.options.prevText);

    this.createNumElement();

    disable = ""
    if(this.options.current === PageTotalNum){
        disable = 'disable'
    }
    this.createElement('next ' + disable, this.options.nextText);
    this.createElement('last ' + disable, this.options.lastText);

    let span = document.createElement('span');
    let i = `<i>${this.options.current}</i> /<i>${PageTotalNum}</i>`;
    span.innerHTML = i;
    this.options.container.appendChild(span)
}

Paging.prototype.createNumElement = function() {
    let min = this.options.current - Math.floor(this.options.PageNum / 2);
    if(min < 1) {
        min = 1;
    }
    let max = min + this.options.PageNum - 1;
    let PageTotalNum = this.getPageTotalNum();
    if (max > PageTotalNum){
        max = PageTotalNum;
    }
    let active = "";
    for(let i = min; i <= max; i ++) {
        if(this.options.current === i) {
            active = 'active';
        }else{
            active = '';
        }
        this.createElement('pagingDiv ' + active, i);
    }
}


Paging.prototype.createElement = function(specialStyle, content) {
    let oDiv = document.createElement('div');
    oDiv.className = specialStyle;
    oDiv.innerText = content;
    this.options.container.appendChild(oDiv);
}

Paging.prototype.getPageTotalNum = function() {
    return Math.ceil(this.options.total / this.options.PageSize)
}
// 点击事件函数
Paging.prototype.PageClick = function() {
    let _this = this;
    let PageTotalNum = this.getPageTotalNum();
    this.options.container.addEventListener('click', function(e) {
        if(e.target.classList.contains('first')){
            _this.toPage(1);
        } else if (e.target.classList.contains('prev')) {
            _this.toPage(_this.options.current - 1);
        } else if (e.target.classList.contains('next')) {
            _this.toPage(_this.options.current + 1);
        } else if (e.target.classList.contains('last')) {
            _this.toPage(PageTotalNum);
        } else if(e.target.classList.contains('pagingDiv')){
            _this.toPage(+e.target.innerText);
        }
    })
}

Paging.prototype.toPage = function (page){
    let PageTotalNum = this.getPageTotalNum();
    if(page < 1) {
        page = 1;
    }
    if(page > PageTotalNum){
        page = PageTotalNum;
    }
    this.options.current = page;
    this.show()
	//this.toAjaxData(page)
}
Paging.prototype.toAjaxData = function (page){
   $.ajax({
   	async: false,
   	url:"company-ajax",
   	type:'GET',
   	dataType: 'json',
   	data:{'test_num':page},
   	success:function(ret){
   		
   		$('#table_head tr:gt(0)').remove();
   		$('#table_head').show();
   		/*
   		如果请求成功 显示表头
   		*/
   		var server_list=[]; //服务列表 用于搜索下拉
   		var public_list=[]; // 版本号列表
   		var title_list=[];// 沉淀标题列表
   		var person_list=[]; // 人员列表
   		/*
   			循环获取 后端返回数据 
   			如果 返回的数据在 定义的列表中没有找到 就加入
   			达到搜索下拉包含全部不重复的值
   		*/
   		$.each(ret, function(i,item){
   			// if(ID_list.indexOf(item.ID)==-1){
   			// 	ID_list.push(item.ID)
   			// }
   			//
   			// if(company_list.indexOf(item.CD_name)==-1){
   			// 	company_list.push(item.CD_name)
   			// }
   			if(server_list.indexOf(item.Server)==-1){
   				industy_list.push(item.Server)
   			}
   			if(public_list.indexOf(item.add_public)==-1){
   				public_list.push(item.add_public)
   			}
   			var Server_name =item.Server;
           	var url ="{% url 'company-info' %}?Server="+Server_name;
   			var tr_new=$('<tr class="order" border="3"></tr>');
   			alert("是这个页面没错");
   			//获得 小对象个数用于table合并
   			
   			tr_new.append(
   					'<td height="20px" width="100px"class="big_table" id="Server">'+'<a data-title="服务信息" data-href="' + url + '" class="c-primary" href="javascript:;">'+item.Server + '</a>' +'</td>'+
   					'<td height="20px" width="100px"class="big_table" id="CD_name">' + item.CD_name+ '</td>'+
   					'<td height="20px" width="100px" class="big_table" id="AddPublic">'+item.add_public+'</td>'+
   					'<td height="20px" width="100px"class="big_table"  id= "person">' + item.person + '</td>'+
   					'<td height="20px" width="100px"class="big_table" id="CreatTime">' + item.create_time + '</td>'+
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
}