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

# 模型管理(道德品质)
@app.route('/customer/customer_ddpz/<type>/<int:id>', methods=['GET'])
def customer_ddpz(type,id):
	#显示布局
	ddpz_level_2 = Rcs_Parameter_Tree.query.filter_by(param_type=type,level_type=2,create_user=current_user.id).all()
	ddpz_level_3 = Rcs_Parameter_Tree.query.filter_by(param_type=type,level_type=3,create_user=current_user.id).all()
	all_select = Rcs_Parameter_Select.query.all()
	#页面数据
	data = Rcs_Application_Ddpz.query.filter_by(application_id=id,create_user=current_user.id).first()
	score = Rcs_Application_Score.query.filter_by(application_id=id,create_user=current_user.id).first()
	return render_template("customer/new_ddpz.html",ddpz_level_2=ddpz_level_2,ddpz_level_3=ddpz_level_3,all_select=all_select,id=id,data=data,score=score)

#道德品质保存
@app.route('/customer/customer_ddpz_save/<int:id>', methods=['POST'])
def customer_ddpz_save(id):     
	total = request.form['score_result'] 
	remark = request.form['score_stop'] 
	score = Rcs_Application_Score.query.filter_by(application_id=id,create_user=current_user.id).first()
	if score:
	    score.ddpz_score=total
	else:
	    Rcs_Application_Score(id,total,"","","",remark).add()
    #道德品质页面form数据保存
	#form json值
	dataTotalSelect = request.form['dataTotalSelect']
	ddpzData = Rcs_Application_Ddpz.query.filter_by(application_id=id,create_user=current_user.id).first()
	if ddpzData:
	    ddpzData.value_2=dataTotalSelect
	else:
	    Rcs_Application_Ddpz(id,"",dataTotalSelect).add()
	db.session.commit()
	return redirect("/customer/customer_ddpz/ddpz/"+str(id))

# 模型管理(生活状况)
@app.route('/customer/customer_shzk/<type>/<int:id>', methods=['GET'])
def customer_shzk(type,id):
	ddpz_level_2 = Rcs_Parameter_Tree.query.filter_by(param_type=type,level_type=2,create_user=current_user.id).all()
	ddpz_level_3 = Rcs_Parameter_Tree.query.filter_by(param_type=type,level_type=3,create_user=current_user.id).all()
	all_select = Rcs_Parameter_Select.query.all()
	#页面数据
	data = Rcs_Application_Shzk.query.filter_by(application_id=id,create_user=current_user.id).first()
	score = Rcs_Application_Score.query.filter_by(application_id=id,create_user=current_user.id).first()
	return render_template("customer/new_shzk.html",ddpz_level_2=ddpz_level_2,ddpz_level_3=ddpz_level_3,all_select=all_select,id=id,data=data,score=score)

#生活状况保存
@app.route('/customer/customer_shzk_save/<int:id>', methods=['POST'])
def customer_shzk_save(id):     
	total = request.form['score_result'] 
	remark = request.form['score_stop'] 
	score = Rcs_Application_Score.query.filter_by(application_id=id,create_user=current_user.id).first()
	if score:
	    score.shzk_score=total
	    if remark:
	    	score.remark=remark
	else:
	    Rcs_Application_Score(id,"","","",total,remark).add()
    #生活状况页面form数据保存
	#form json值
	dataTotalSelect = request.form['dataTotalSelect']
	ddpzData = Rcs_Application_Shzk.query.filter_by(application_id=id,create_user=current_user.id).first()
	if ddpzData:
	    ddpzData.value_2=dataTotalSelect
	else:
	    Rcs_Application_Shzk(id,"",dataTotalSelect,"").add()
	db.session.commit()
	return redirect("/customer/customer_shzk/shzk/"+str(id))

# 模型管理(经营状况)
@app.route('/customer/customer_jyzk/<type>/<int:id>', methods=['GET'])
def customer_jyzk(type,id):
	ddpz_level_2 = Rcs_Parameter_Tree.query.filter_by(param_type=type,level_type=2,create_user=current_user.id).all()
	ddpz_level_3 = Rcs_Parameter_Tree.query.filter_by(param_type=type,level_type=3,create_user=current_user.id).all()
	all_select = Rcs_Parameter_Select.query.all()
	#页面数据
	data = Rcs_Application_Jyzk.query.filter_by(application_id=id,create_user=current_user.id).first()
	score = Rcs_Application_Score.query.filter_by(application_id=id,create_user=current_user.id).first()
	return render_template("customer/new_jyzk.html",ddpz_level_2=ddpz_level_2,ddpz_level_3=ddpz_level_3,all_select=all_select,id=id,data=data,score=score)

#经营状况保存
@app.route('/customer/customer_jyzk_save/<int:id>', methods=['POST'])
def customer_jyzk_save(id):     
	total = request.form['score_result'] 
	remark = request.form['score_stop'] 
	score = Rcs_Application_Score.query.filter_by(application_id=id,create_user=current_user.id).first()
	if score:
	    score.jyzk_score=total
	else:
	    Rcs_Application_Score(id,"","",total,"",remark).add()
    #经营状况页面form数据保存
	#form json值
	dataTotalSelect = request.form['dataTotalSelect']
	ddpzData = Rcs_Application_Jyzk.query.filter_by(application_id=id,create_user=current_user.id).first()
	if ddpzData:
	    ddpzData.value_2=dataTotalSelect
	else:
	    Rcs_Application_Jyzk(id,"",dataTotalSelect).add()
	db.session.commit()
	return redirect("/customer/customer_jyzk/jyzk/"+str(id))