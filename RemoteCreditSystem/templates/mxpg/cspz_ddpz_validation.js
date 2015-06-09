var validator = $("#iframeForm").validate({
	rules:
    { 
		jtqk:{required:true}
     },
messages:
    {
		jtqk:{required:"不能为空"}
   },
	errorPlacement : function(error, element) {
		element.after(error);
		if(layout){
			layout.resizeLayout();
		}
	}
});