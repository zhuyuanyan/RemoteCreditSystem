# coding:utf-8
import hashlib

from RemoteCreditSystem import User
from flask import request, render_template,flash,redirect
from flask.ext.login import login_user, logout_user, current_user, login_required
from RemoteCreditSystem import app
from RemoteCreditSystem import db
from RemoteCreditSystem.config import PER_PAGE

from RemoteCreditSystem.models import Rcs_Parameter_Tree
from RemoteCreditSystem.models import Rcs_Parameter_Select
from RemoteCreditSystem.models.system_usage.Rcs_Application_Jyzk import Rcs_Application_Jyzk
from RemoteCreditSystem.models.system_usage.Rcs_Application_Ddpz import Rcs_Application_Ddpz
from RemoteCreditSystem.models.system_usage.Rcs_Application_Shzk import Rcs_Application_Shzk
from RemoteCreditSystem.models.system_usage.Rcs_Application_Score import Rcs_Application_Score
from RemoteCreditSystem.models.system_usage.Rcs_Application_Info import Rcs_Application_Info
from RemoteCreditSystem.models.system_usage.Rcs_Application_Jcjy import Rcs_Application_Jcjy

# 模型管理(道德品质)
@app.route('/customer/customer_ddpz/<type>/<int:id>', methods=['GET'])
def customer_ddpz(type,id):
	#显示布局
	ddpz_level = Rcs_Parameter_Tree.query.filter(" param_type='"+type+"' and id in (select tree_id from rcs_parameter_select)").all()
	all_select = Rcs_Parameter_Select.query.all()

	#页面数据
	data = Rcs_Application_Ddpz.query.filter_by(application_id=id).first()
	score = Rcs_Application_Score.query.filter_by(application_id=id).first()
	return render_template("customer/new_ddpz.html",ddpz_level=ddpz_level,all_select=all_select,id=id,data=data,score=score)

#道德品质保存
@app.route('/customer/customer_ddpz_save/<int:id>', methods=['POST'])
def customer_ddpz_save(id):     
	total = request.form['score_result'] 
	remark = request.form['score_stop'] 
	score = Rcs_Application_Score.query.filter_by(application_id=id).first()
	if score:
	    score.ddpz_score=total
	else:
	    Rcs_Application_Score(id,total,"","","",remark).add()
    #道德品质页面form数据保存
	#form json值
	dataTotalSelect = request.form['dataTotalSelect']
	ddpzData = Rcs_Application_Ddpz.query.filter_by(application_id=id).first()
	if ddpzData:
	    ddpzData.value_2=dataTotalSelect
	else:
	    Rcs_Application_Ddpz(id,"",dataTotalSelect).add()
	db.session.commit()
	return redirect("/customer/customer_ddpz/ddpz/"+str(id))

# 模型管理(生活状况)
@app.route('/customer/customer_shzk/<type>/<int:id>', methods=['GET'])
def customer_shzk(type,id):
	#显示布局
	ddpz_level = Rcs_Parameter_Tree.query.filter(" param_type='"+type+"' and id in (select tree_id from rcs_parameter_select)").all()
	all_select = Rcs_Parameter_Select.query.all()



	#页面数据
	data = Rcs_Application_Ddpz.query.filter_by(application_id=id).first()
	score = Rcs_Application_Score.query.filter_by(application_id=id).first()
	return render_template("customer/new_shzk.html",ddpz_level=ddpz_level,all_select=all_select,id=id,data=data,score=score)
#生活状况保存
@app.route('/customer/customer_shzk_save/<int:id>', methods=['POST'])
def customer_shzk_save(id):     
	total = request.form['score_result'] 
	remark = request.form['score_stop'] 
	score = Rcs_Application_Score.query.filter_by(application_id=id).first()
	if score:
	    score.shzk_score=total
	    if remark:
	    	score.remark=remark
	else:
	    Rcs_Application_Score(id,"","","",total,remark).add()
    #生活状况页面form数据保存
	#form json值
	dataTotalSelect = request.form['dataTotalSelect']
	ddpzData = Rcs_Application_Shzk.query.filter_by(application_id=id).first()
	if ddpzData:
	    ddpzData.value_2=dataTotalSelect
	else:
	    Rcs_Application_Shzk(id,"",dataTotalSelect,"").add()
	db.session.commit()
	return redirect("/customer/customer_shzk/shzk/"+str(id))

# 模型管理(经营状况)
@app.route('/customer/customer_jyzk/<type>/<int:id>', methods=['GET'])
def customer_jyzk(type,id):
	#显示布局
	ddpz_level = Rcs_Parameter_Tree.query.filter(" param_type='"+type+"' and id in (select tree_id from rcs_parameter_select)").all()
	all_select = Rcs_Parameter_Select.query.all()



	#页面数据
	data = Rcs_Application_Ddpz.query.filter_by(application_id=id).first()
	score = Rcs_Application_Score.query.filter_by(application_id=id).first()
	return render_template("customer/new_jyzk.html",ddpz_level=ddpz_level,all_select=all_select,id=id,data=data,score=score)
#经营状况保存
@app.route('/customer/customer_jyzk_save/<int:id>', methods=['POST'])
def customer_jyzk_save(id):     
	total = request.form['score_result'] 
	remark = request.form['score_stop'] 
	score = Rcs_Application_Score.query.filter_by(application_id=id).first()
	if score:
	    score.jyzk_score=total
	else:
	    Rcs_Application_Score(id,"","",total,"",remark).add()
    #经营状况页面form数据保存
	#form json值
	dataTotalSelect = request.form['dataTotalSelect']
	ddpzData = Rcs_Application_Jyzk.query.filter_by(application_id=id).first()
	if ddpzData:
	    ddpzData.value_2=dataTotalSelect
	else:
	    Rcs_Application_Jyzk(id,"",dataTotalSelect).add()
	db.session.commit()
	return redirect("/customer/customer_jyzk/jyzk/"+str(id))

#查看评估报告
@app.route('/mxpg/show_pgbg/<int:id>', methods=['GET'])
def show_pgbg(id):    
    score = Rcs_Application_Score.query.filter_by(application_id=id).first()
    info = Rcs_Application_Info.query.filter_by(id=id).first()
    jcjy = Rcs_Application_Jcjy.query.filter_by(application_id=id).first()

    pet = ""
    #获取道德品质统计
    ddpz = Rcs_Application_Ddpz.query.filter_by(application_id=id).first()
    ddpz_null = 0
    if ddpz:
    	value = ddpz.value_2.split(",")
    	for obj in value:
    		if "@@无数据" in obj:
    			ddpz_null+=1
    	pet+= "道德品质:"+str(ddpz_null)+"/"+ str(len(value))+","

    #获取生活状况统计
    shzk = Rcs_Application_Shzk.query.filter_by(application_id=id).first()
    shzk_null = 0
    if shzk:
    	value = shzk.value_2.split(",")
    	for obj in value:
    		if "@@无数据" in obj:
    			shzk_null+=1
    	pet += "生活状况:"+str(shzk_null)+"/"+ str(len(value))+","

    #获取经营状况统计
    jyzk = Rcs_Application_Jyzk.query.filter_by(application_id=id).first()
    jyzk_null = 0
    if jyzk:
    	value = jyzk.value_2.split(",")
    	for obj in value:
    		if "@@无数据" in obj:
    			jyzk_null+=1
    	pet += "经营状况:"+str(jyzk_null)+"/"+ str(len(value))

    return render_template("mxpg/show_pgbg.html",score=score,info=info,jcjy=jcjy,pet=pet)