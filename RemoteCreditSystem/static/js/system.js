// -------------权限管理------------- begin
//功能权限select管理
function change_select(obj,classname){
    if(obj.value == "0"){
        $("." + classname).each(function() {
            $(this).empty();
            $(this).append("<option value='0'>无权限</option>");
        });
    }
    if(obj.value == "1"){
        $("." + classname).each(function() {
            $(this).empty();
            $(this).append("<option value='1'>查询</option><option value='0'>无权限</option>");
        });
    }
    if(obj.value == "2"){
        $("." + classname).each(function() {
            $(this).empty();
            $(this).append("<option value='2'>维护</option><option value='1'>查询</option><option value='0'>无权限</option>");
        });
    }
}


// -------------权限管理------------- end

// ------------机构管理------------- begin

// ------------机构管理------------- end

// -------------数据字典------------- begin

// -------------数据字典------------- end