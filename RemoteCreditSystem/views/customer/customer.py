# coding:utf-8
import hashlib

from RemoteCreditSystem import User
from flask import request, render_template,flash,redirect
from flask.ext.login import login_user, logout_user, current_user, login_required
from RemoteCreditSystem import app
from RemoteCreditSystem import db
from RemoteCreditSystem.config import PER_PAGE
import RemoteCreditSystem.helpers as helpers

from RemoteCreditSystem.models import Rcs_Parameter_Tree
from RemoteCreditSystem.models import Rcs_Parameter_Select
from RemoteCreditSystem.models.system_usage.Rcs_Application_Jyzk import Rcs_Application_Jyzk
from RemoteCreditSystem.models.system_usage.Rcs_Application_Ddpz import Rcs_Application_Ddpz
from RemoteCreditSystem.models.system_usage.Rcs_Application_Shzk import Rcs_Application_Shzk
from RemoteCreditSystem.models.system_usage.Rcs_Application_Score import Rcs_Application_Score
from RemoteCreditSystem.models.system_usage.Rcs_Application_Info import Rcs_Application_Info
from RemoteCreditSystem.models.system_usage.Rcs_Application_Jcjy import Rcs_Application_Jcjy
from RemoteCreditSystem.models.system_usage.Rcs_Parameter import Rcs_Parameter

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
	# total = request.form['score_result'] 
	# remark = request.form['score_stop'] 
	# score = Rcs_Application_Score.query.filter_by(application_id=id).first()
	# tree = Rcs_Parameter_Tree.query.filter_by(level_type=1).all()

	# if score:
	# 	if remark:
	# 		score.remark=remark
	# 		score.ddpz_score=0
	# 		score.total_approve =0
	# 	else:
	# 		score.ddpz_score=float('%.2f'% float(total))
	# 		score.remark=""
	# 		if score.ddpz_score and score.hknl_score and score.jyzk_score and score.shzk_score:
	# 			totalScore = float(score.ddpz_score)*float(score.hknl_score)*float(score.jyzk_score)*float(score.shzk_score)
	# 			for obj in tree:
	# 				totalScore = totalScore*float(obj.weight)
	# 			score.total_approve = float('%.2f'% totalScore)
	# else:
	#     Rcs_Application_Score(id,float('%.2f'% float(total)),"","","",remark,"").add()
    #道德品质页面form数据保存
	#form json值

	form_data = request.form['form_data']
	dataTotalSelect = request.form['selectData']
	ddpzData = Rcs_Application_Ddpz.query.filter_by(application_id=id).first()
	if ddpzData:
	    ddpzData.value_2=dataTotalSelect
	    ddpzData.value_select = form_data
	else:
	    Rcs_Application_Ddpz(id,"",dataTotalSelect,form_data).add()
	db.session.commit()
	return redirect("/customer/customer_ddpz/ddpz/"+str(id))

# 模型管理(生活状况)
@app.route('/customer/customer_shzk/<type>/<int:id>', methods=['GET'])
def customer_shzk(type,id):
	#显示布局
	ddpz_level = Rcs_Parameter_Tree.query.filter(" param_type='"+type+"' and id in (select tree_id from rcs_parameter_select)").all()
	all_select = Rcs_Parameter_Select.query.all()



	#页面数据
	data = Rcs_Application_Shzk.query.filter_by(application_id=id).first()
	score = Rcs_Application_Score.query.filter_by(application_id=id).first()
	return render_template("customer/new_shzk.html",ddpz_level=ddpz_level,all_select=all_select,id=id,data=data,score=score)
#生活状况保存
@app.route('/customer/customer_shzk_save/<int:id>', methods=['POST'])
def customer_shzk_save(id):     
	# total = request.form['score_result'] 
	# remark = request.form['score_stop'] 
	# score = Rcs_Application_Score.query.filter_by(application_id=id).first()
	# tree = Rcs_Parameter_Tree.query.filter_by(level_type=1).all()
	# if score:
	#     if remark:
	#     	score.remark=remark
	#     	score.shzk_score=0
	#     	score.total_approve =0
	#     else:
	# 		score.shzk_score=float('%.2f'% float(total))
	# 		score.remark=""
	# 		if score.ddpz_score and score.hknl_score and score.jyzk_score and score.shzk_score:
	# 			totalScore = float(score.ddpz_score)*float(score.hknl_score)*float(score.jyzk_score)*float(score.shzk_score)
	# 			for obj in tree:
	# 				totalScore = totalScore*float(obj.weight)
	# 			score.total_approve = float('%.2f'% totalScore)
	# else:
	#     Rcs_Application_Score(id,"","","",float('%.2f'% float(total)),remark,"").add()
    #生活状况页面form数据保存
	#form json值
	form_data = request.form['form_data']
	dataTotalSelect = request.form['selectData']
	ddpzData = Rcs_Application_Shzk.query.filter_by(application_id=id).first()
	if ddpzData:
	    ddpzData.value_2=dataTotalSelect
	    ddpzData.value_select = form_data
	else:
	    Rcs_Application_Shzk(id,"",dataTotalSelect,"",form_data).add()
	db.session.commit()
	return redirect("/customer/customer_shzk/shzk/"+str(id))

# 模型管理(经营状况)
@app.route('/customer/customer_jyzk/<type>/<int:id>', methods=['GET'])
def customer_jyzk(type,id):
	#显示布局
	ddpz_level = Rcs_Parameter_Tree.query.filter(" param_type='"+type+"' and id in (select tree_id from rcs_parameter_select)").all()
	all_select = Rcs_Parameter_Select.query.all()



	#页面数据
	data = Rcs_Application_Jyzk.query.filter_by(application_id=id).first()
	score = Rcs_Application_Score.query.filter_by(application_id=id).first()
	return render_template("customer/new_jyzk.html",ddpz_level=ddpz_level,all_select=all_select,id=id,data=data,score=score)
#经营状况保存
@app.route('/customer/customer_jyzk_save/<int:id>', methods=['POST'])
def customer_jyzk_save(id):     
	# total = request.form['score_result'] 
	# remark = request.form['score_stop'] 
	# score = Rcs_Application_Score.query.filter_by(application_id=id).first()
	# tree = Rcs_Parameter_Tree.query.filter_by(level_type=1).all()
	# if score:
	# 	if remark:
	# 		score.remark=remark
	# 		score.jyzk_score=0
	# 		score.total_approve =0
	# 	else:	
	# 		score.jyzk_score=float('%.2f'% float(total))
	# 		score.remark=""
	# 		if score.ddpz_score and score.hknl_score and score.jyzk_score and score.shzk_score:
	# 			totalScore = float(score.ddpz_score)*float(score.hknl_score)*float(score.jyzk_score)*float(score.shzk_score)
	# 			for obj in tree:
	# 				totalScore = totalScore*float(obj.weight)
	# 			score.total_approve = float('%.2f'% float(totalScore))  
	# else:
	#     Rcs_Application_Score(id,"","",float('%.2f'% float(total)),"",remark,"").add()
    #经营状况页面form数据保存
	#form json值
	form_data = request.form['form_data']
	dataTotalSelect = request.form['selectData']
	ddpzData = Rcs_Application_Jyzk.query.filter_by(application_id=id).first()
	if ddpzData:
	    ddpzData.value_2=dataTotalSelect
	    ddpzData.value_select = form_data
	else:
	    Rcs_Application_Jyzk(id,"",dataTotalSelect,form_data).add()
	db.session.commit()
	return redirect("/customer/customer_jyzk/jyzk/"+str(id))

#查看评估报告
@app.route('/mxpg/show_pgbg/<int:id>', methods=['GET'])
def show_pgbg(id):    
    score = Rcs_Application_Score.query.filter_by(application_id=id).first()
    info = Rcs_Application_Info.query.filter_by(id=id).first()
    tree = Rcs_Parameter_Tree.query.filter_by(level_type=1).all()
    if score:
	    for obj in tree:
			if 'ddpz' in obj.param_type:
				if score.ddpz_score:
					score.ddpz_score = float(obj.weight)*float(score.ddpz_score)
			if 'shzk' in obj.param_type:
				if score.shzk_score:
					score.shzk_score = float(obj.weight)*float(score.shzk_score)
			if 'jyzk' in obj.param_type:
				if score.jyzk_score:
					score.jyzk_score = float(obj.weight)*float(score.jyzk_score)
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

    #获取生存状况统计
    shzk = Rcs_Application_Shzk.query.filter_by(application_id=id).first()
    shzk_null = 0
    if shzk:
    	value = shzk.value_2.split(",")
    	for obj in value:
    		if "@@无数据" in obj:
    			shzk_null+=1
    	pet += "生存状况:"+str(shzk_null)+"/"+ str(len(value))+","

    #获取经营状况统计
    jyzk = Rcs_Application_Jyzk.query.filter_by(application_id=id).first()
    jyzk_null = 0
    if jyzk:
    	value = jyzk.value_2.split(",")
    	for obj in value:
    		if "@@无数据" in obj:
    			jyzk_null+=1
    	pet += "经营状况:"+str(jyzk_null)+"/"+ str(len(value))


    return render_template("mxpg/show_pgbg.html",score=score,info=info,pet=pet)

#计算总分值
@app.route('/parameter/scoreTotal/<score>', methods=['GET'])
def scoreTotal(score):
	pet = score.split(",")
	value = 0
	totalValue = 0
	for obj in pet:
		if "@" not in obj:
			select = Rcs_Parameter_Select.query.filter_by(id=obj).first()
			tree = Rcs_Parameter_Tree.query.filter_by(id=select.tree_id).first()
			value = (float(select.score)/100)*float(tree.weight)
			totalValue+=count(tree.id,value)
		else:
			#无数据默认为满分值
			tree_id=obj.split("@")[0]
			tree = Rcs_Parameter_Tree.query.filter_by(id=tree_id).first()
			value = float(tree.weight)
			totalValue+=count(tree.id,value)
	return str(totalValue)


#递归计算select分值
def count(id,value):
	#查找当前节点
	tree = Rcs_Parameter_Tree.query.filter_by(id=id).first()
	if tree.level_type:
		if int(tree.level_type)!=1:
			#查找父节点
			parent = Rcs_Parameter_Tree.query.filter_by(id=tree.pId).first()
			#查找父节点下所有子节点
			child_all = Rcs_Parameter_Tree.query.filter_by(pId=parent.id).all()
			total = 0
			for obj in child_all:
				total+=float(obj.weight)
			if int(parent.level_type)==1:
				value = float(value)/float(total)
			else:
				value = float(parent.weight)*float(value)/float(total)
			return count(tree.pId,value)
		else:
			return value


#后台计算所有评估值
@app.route('/customer/access/<int:id>', methods=['POST'])
def access(id):
	score = Rcs_Application_Score.query.filter_by(application_id=id).first()
	ddpz = Rcs_Application_Ddpz.query.filter_by(application_id=id).first()
	shzk = Rcs_Application_Shzk.query.filter_by(application_id=id).first()
	jyzk = Rcs_Application_Jyzk.query.filter_by(application_id=id).first()
	info = Rcs_Application_Info.query.filter_by(id=id).first()
	parameter_tree = Rcs_Parameter_Tree.query.filter_by(level_type=1).all()
	totalValue_ddpz = 0
	totalValue_shzk = 0
	totalValue_jyzk = 0
	totalValue_hknl = 0
	paramer_value=0
	totalScore = 0
	remark = ''
	if ddpz:
		if ddpz.value_select is not None:
			value = 0
			for obj in ddpz.value_select.split("&"):
				ids = obj.split("=")[1]
				if "*" not in ids:
					select = Rcs_Parameter_Select.query.filter_by(id=ids).first()
					tree = Rcs_Parameter_Tree.query.filter_by(id=select.tree_id).first()
					if "禁入" in select.score:
						totalValue_ddpz = 0
						remark+=tree.name+"为禁入,"
						break
					else:
						value = (float(select.score)/100)*float(tree.weight)
						totalValue_ddpz+=count(tree.id,value)
				else:
					#无数据默认为满分值
					tree_id=ids.split("*")[0]
					tree = Rcs_Parameter_Tree.query.filter_by(id=tree_id).first()
					value = float(tree.weight)
					totalValue_ddpz+=count(tree.id,value)
	if shzk:
		if shzk.value_select is not None:
			value = 0
			for obj in shzk.value_select.split("&"):
				ids = obj.split("=")[1]
				if "*" not in ids:
					select = Rcs_Parameter_Select.query.filter_by(id=ids).first()
					tree = Rcs_Parameter_Tree.query.filter_by(id=select.tree_id).first()
					if "禁入" in select.score:
						totalValue_shzk = 0
						remark+=tree.name+"为禁入,"
						break
					else:
						value = (float(select.score)/100)*float(tree.weight)
						totalValue_shzk+=count(tree.id,value)
				else:
					#无数据默认为满分值
					tree_id=ids.split("*")[0]
					tree = Rcs_Parameter_Tree.query.filter_by(id=tree_id).first()
					value = float(tree.weight)
					totalValue_shzk+=count(tree.id,value)
	if jyzk:
		if jyzk.value_select is not None:
			value = 0
			for obj in jyzk.value_select.split("&"):
				ids = obj.split("=")[1]
				if "*" not in ids:
					select = Rcs_Parameter_Select.query.filter_by(id=ids).first()
					tree = Rcs_Parameter_Tree.query.filter_by(id=select.tree_id).first()
					if "禁入" in select.score:
						totalValue_jyzk = 0
						remark+=tree.name+"为禁入,"
						break
					else:
						value = (float(select.score)/100)*float(tree.weight)
						totalValue_jyzk+=count(tree.id,value)
				else:
					#无数据默认为满分值
					tree_id=ids.split("*")[0]
					tree = Rcs_Parameter_Tree.query.filter_by(id=tree_id).first()
					value = float(tree.weight)
					totalValue_jyzk+=count(tree.id,value)
	#计算还款能力
	if info.model_type:
		#标准
		if int(info.model_type)==2:	
			#获取还款能力参数配置数据
			parm = Rcs_Parameter.query.filter_by(parameter_name='hknl').first()
			if parm:
			    value = parm.parameter_value.split(',')
			    #与参数配置相对应
			    paramer_value = value[140]
			    totalValue_hknl = float(paramer_value)*float(score.month_profit)
		#传统
		elif int(info.model_type)==1:
			totalValue_hknl = score.month_profit

	#计算总授信额度
	totalScore = float('%.3f'% float(totalValue_ddpz))*float('%.3f'% float(totalValue_shzk))*float('%.3f'% float(totalValue_jyzk))*float('%.3f'% float(totalValue_hknl))
	for obj in parameter_tree:
		totalScore = totalScore*float(obj.weight)

	if len(remark)>0:
		remark = remark[:-1]
	if score:
		score.ddpz_score = float('%.3f'% float(totalValue_ddpz))
		score.shzk_score = float('%.3f'% float(totalValue_shzk))
		score.jyzk_score = float('%.3f'% float(totalValue_jyzk))
		score.hknl_score = float('%.3f'% float(totalValue_hknl))   
		score.total_approve = float('%.2f'% float(totalScore))
		score.remark = remark
	else:
		Rcs_Application_Score(id,totalValue_ddpz,totalValue_hknl,totalValue_jyzk,totalValue_shzk,remark,float('%.2f'% float(totalScore)),'').add()
	db.session.commit()
	return helpers.show_result_success('') # 返回json


#资产负债（小微贷）
@app.route('/customer/zcfzzk/<int:id>', methods=['GET'])
def zcfzzk(id):   
    return render_template("customer/new_zcfzzk.html",id=id)

#利润表（小微贷）
@app.route('/customer/lrb/<int:id>', methods=['GET'])
def lrb(id):        

    return render_template("customer/new_lrb.html",id=id)

#现金流量（小微贷）
@app.route('/customer/xjl/<int:id>', methods=['GET'])
def xjl(id): 


	return render_template("customer/new_xjl.html",id=id)