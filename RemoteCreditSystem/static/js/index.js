var submitFlag = true;//防止重复提交$(document).ready(function(){	setInterval(function(){$("#time").html(showTime)},1000); //显示时间	})function creattime(i){//不满两位前面补“0”	if(i<10)		{i="0"+i};	return i;}function showTime(){	var date=new Date();	var nian=date.getFullYear();//年	var month=creattime(date.getMonth()+1);//月	var da=creattime(date.getDate());//日	var day=date.getDay();//星期几	var hour=creattime(date.getHours());//时	var minute=creattime(date.getMinutes());//分	var second=creattime(date.getSeconds());//秒	var txt;	switch(day)	{		case 1:			txt="一"			break		case 2:			txt="二"			break		case 3:			txt="三"			break		case 4:			txt="四"			break		case 5:			txt="五"			break		case 6:			txt="六"			break		case 0:			txt="日"			break		default:			sj.innerHTML="出错了"	}	times=nian+"年"+month+"月"+da+"日&nbsp;&nbsp;星期"+txt+"&nbsp;&nbsp;"+hour+":"+minute+":"+second		return times; }//左侧导航function changeNav(obj,num){	var src="../static/img/"+num+"_active.png"	var images=$(obj).parent().find(".tip")			if($(obj).find("li").length!=0){//有二级菜单			$(".second-nav li").click(function(){//点击二级菜单时执行			for(i=0;i<images.length;i++){				images[i].src="../static/img/"+(i+1)+".png"//所有一级导航的图片变成灰色			}			images[num-1].src=src;//二级菜单所在一级导航的图片变有色			$(".nav li").attr("class","");//所有一级菜单恢复普通状态，不显示蓝三角			$(".second-nav li").attr("class","");//二级菜单中的列背景为白色			$(this).attr("class","active");//点击的二级菜单项显示蓝三角		});	}	else{//无二级菜单		for(i=0;i<images.length;i++){			images[i].src="../static/img/"+(i+1)+".png"//所有一级导航的图片变成灰色		}		images[num-1].src=src;//点击的一级导航的图片变有色		$(".nav li").attr("class","");//所有一级菜单恢复普通状态，不显示蓝三角				$(obj).attr("class","active");//点击的一级菜单显示蓝三角		$(".second-nav li").attr("class","");//二级菜单中的列背景为白色	}}function showMenu(num){//显示隐藏二级菜单	for(i=1;i<100;i++){		if(i!=num)			$("#ul"+i).slideUp("slow")//隐藏除点击项外所有二级菜单		else{			if($("#ul"+num).css("display")=="none")//点击项处于隐藏状态				$("#ul"+num).slideDown("slow")			else//点击项处于显示状态				$("#ul"+num).slideUp("slow")		}	}	}//切换iframe里的内容用于主页面function changeiframe(page){	$("#content_frame").attr("src",page);}//切换iframe里的内容用于iframe内部页面	function iframe(page){	//window.location.href = "/" + page;   window.location.href =  page;}function changeTab(obj,id){//首页Tab	$(".tab li").attr("class","");	$(obj).attr("class","active");	$(".tabContent .tabs").attr("class","tabs");	$("#"+id).attr("class","tabs active");}	function changeItem(obj){//首页折叠待办	var em=$(obj).find("em").attr("class")	if(em=="icon-up"){		$(obj).find("em").attr("class","icon-down");		$(obj).parent().find(".itemList").slideUp("slow");	}	if(em=="icon-down"){		$(obj).find("em").attr("class","icon-up");		$(obj).parent().find(".itemList").slideDown("slow");	}	if(em=="icon-up-small"){		$(obj).find("em").attr("class","icon-down-small");		$(obj).parent().find(".itemList").slideUp("slow");	}	if(em=="icon-down-small"){		$(obj).find("em").attr("class","icon-up-small");		$(obj).parent().find(".itemList").slideDown("slow");	}}function checkTable(obj){//点击表格某行选中该项	$(obj).find('input[type=radio]').attr('checked','checked')}function changeShow(obj){//折叠box	if($(obj).attr("class")=="box activeBox"){		$(obj).attr("class","box");		$(obj).find(".zdBox").attr("src","../static/img/left.png")	}	else{		$(obj).attr("class","box activeBox");		$(obj).find(".zdBox").attr("src","../static/img/down.png")	}}function Tabs(obj,id){//tabList页面	$(".tabList li").attr("class","");	$(obj).attr("class","active");	$(".tabContentList .tabs").hide();	$("#"+id).show();}	function setTimeOut(){    setTimeout(function(){        $(".alert-success").fadeOut("slow");        $(".alert-error").fadeOut("slow");    },2000)}function updateAllDOMFields(theForm) {	var inputNodes = getAllFormFields(theForm);	for (x = 0; x < inputNodes.length; x++) {		var theNode = inputNodes[x];		updateDOMField(theNode);	}}function updateDOMField(inputField) {    // if the inputField ID string has been passed in, get the inputField object    if (typeof inputField == "string") {        inputField = document.getElementById(inputField);    }         if (inputField.type == "select-one") {        for (var i=0; i<inputField.options.length; i++) {            if (i == inputField.selectedIndex) {                    inputField.options[i].setAttribute("selected","selected");            } else {                inputField.options[i].removeAttribute("selected");            }        }    } else if (inputField.type == "select-multiple") {        for (var i=0; i<inputField.options.length; i++) {            if (inputField.options[i].selected) {                inputField.options[i].setAttribute("selected","selected");            } else {                inputField.options[i].removeAttribute("selected");            }        }    } else if (inputField.type == "text") {        inputField.setAttribute("value",inputField.value);    } else if (inputField.type == "hidden") {        inputField.setAttribute("value",inputField.value);    } else if (inputField.type == "textarea") {        var text = inputField.value;        inputField.innerHTML = text;        inputField.setAttribute("value", text);    } else if (inputField.type == "checkbox") {        if (inputField.checked) {            inputField.setAttribute("checked","checked");        } else {            inputField.removeAttribute("checked");        }    } else if (inputField.type == "radio") {        var radioNames = document.getElementsByName(inputField.name);        for(var i=0; i < radioNames.length; i++) {            if (radioNames[i].checked) {                radioNames[i].setAttribute("checked","checked");            } else {                radioNames[i].removeAttribute("checked");            }        }    }}function getAllFormFields(theForm) {	try {		var inputFields = theForm.getElementsByTagName("input");		var selectFields = theForm.getElementsByTagName("select");		var textFields = theForm.getElementsByTagName("textarea");		var array = new Array(inputFields + selectFields + textFields);		for (i = 0; i < array.length; i++) {			for (x = 0; x < inputFields.length; x++) {				array[i] = inputFields[x];				i++			}			for (a = 0; a < selectFields.length; a++) {				array[i] = selectFields[a];				i++			}			for (t = 0; t < textFields.length; t++) {				//debug("Text box Found" + textFields.name);				array[i] = textFields[t];				i++			}		}	} catch (e) {		alert("Error when evoking getAllFormFields(): \nSomething is probably wrong with the form you passed in\n\n"				+ e.message)	}	return array;}