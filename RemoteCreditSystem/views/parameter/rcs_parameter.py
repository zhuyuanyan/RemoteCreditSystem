# coding:utf-8
from RemoteCreditSystem import db,app
from RemoteCreditSystem.config import logger
import RemoteCreditSystem.helpers as helpers
import datetime
import json

from flask import Module, session, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user

from RemoteCreditSystem.models import Rcs_Parameter_Tree
from RemoteCreditSystem.models import Rcs_Parameter_Select


# 模型参数管理(道德品质)
@app.route('/parameter/model_ddpz', methods=['GET'])
def model_ddpz():
	return render_template("parameter/model_parameter_ddpz.html")

# 模型参数管理(生活状况)
@app.route('/parameter/model_shzk', methods=['GET'])
def model_shzk():
	return render_template("parameter/model_parameter_shzk.html")

# 模型参数管理(经营状况)
@app.route('/parameter/model_jyzk', methods=['GET'])
def model_jyzk():
	return render_template("parameter/model_parameter_jyzk.html")

#左侧加载树
@app.route('/parameter/show_tree/<param_type>', methods=['POST'])
def show_tree(param_type):
	orgs = Rcs_Parameter_Tree.query.filter("pId is null").order_by("id").all()
	orgs_list = []
	if orgs:
		for obj in orgs:
			sql = "FIND_IN_SET(id ,getParamList('"+str(obj.id)+"')) and param_type='"+str(param_type)+"'"
			orgs_list = Rcs_Parameter_Tree.query.filter(sql).order_by("id").all()

	for obj in orgs_list:
		obj.open = 1
	orgs_json = helpers.show_result_content(orgs_list)
	orgs_json_obj = json.loads(orgs_json)
	return json.dumps(orgs_json_obj)# 返回json

#右边显示列表
@app.route('/parameter/show_row/<param_type>/<int:p_id>', methods=['GET'])
def get_project_docs(param_type,p_id):
	select = Rcs_Parameter_Select.query.filter_by(tree_id=p_id).order_by("id").all()
	if select:
		for obj in select:
			obj.style = 2
		return helpers.show_result_content(select) # 返回json
	param = Rcs_Parameter_Tree.query.filter_by(pId=p_id,param_type=param_type).order_by("id").all()
	for obj in param:
		obj.style = 1
	return helpers.show_result_content(param) # 返回json

#新增模型项页面
@app.route('/parameter/add_tree/<int:p_id>', methods=['GET'])
def add_tree(p_id):

	return render_template("parameter/model_tree_add.html",p_id=p_id)

#新增模型项页面save
@app.route('/parameter/add_tree_save/<int:p_id>', methods=['POST'])
def add_tree_save(p_id):
	try:
		name = request.form["name"]
		weight = request.form["weight"]
		tree = Rcs_Parameter_Tree.query.filter_by(id=p_id).first()
		Rcs_Parameter_Tree(tree.param_type,name,p_id,weight,int(tree.level_type)+1).add()
		db.session.commit()
		# 消息闪现
		flash('保存成功','success')
	except:
		# 回滚
		db.session.rollback()
		logger.exception('exception')
		# 消息闪现
		flash('保存失败','error')
	return redirect("/parameter/model_"+tree.param_type)

#修改模型项页面
@app.route('/parameter/edit_tree/<int:p_id>', methods=['GET'])
def edit_tree(p_id):
	tree = Rcs_Parameter_Tree.query.filter_by(id=p_id).first()
	return render_template("parameter/model_tree_edit.html",tree=tree)

#修改模型项页面save
@app.route('/parameter/edit_tree_save/<int:p_id>', methods=['POST'])
def edit_tree_save(p_id):
	try:
		name = request.form["name"]
		weight = request.form["weight"]
		tree = Rcs_Parameter_Tree.query.filter_by(id=p_id).first()
		tree.name = name
		tree.weight = weight
		db.session.commit()
		# 消息闪现
		flash('修改成功','success')
	except:
		# 回滚
		db.session.rollback()
		logger.exception('exception')
		# 消息闪现
		flash('修改失败','error')
	return redirect("/parameter/model_"+tree.param_type)

#新增模型值页面
@app.route('/parameter/add_select/<int:p_id>', methods=['GET'])
def add_select(p_id):

	return render_template("parameter/model_select_add.html",p_id=p_id)

#新增模型值页面save
@app.route('/parameter/add_select_save/<int:p_id>', methods=['POST'])
def add_select_save(p_id):
	try:
		tree = Rcs_Parameter_Tree.query.filter_by(id=p_id).first()
		name = request.form["name"]
		score = request.form["score"]
		Rcs_Parameter_Select(p_id,name,score).add()
		db.session.commit()
		# 消息闪现
		flash('保存成功','success')
	except:
		# 回滚
		db.session.rollback()
		logger.exception('exception')
		# 消息闪现
		flash('保存失败','error')
	return redirect("/parameter/model_"+tree.param_type)

#修改模型值页面
@app.route('/parameter/edit_select/<int:p_id>', methods=['GET'])
def edit_select(p_id):
	select = Rcs_Parameter_Select.query.filter_by(id=p_id).first()
	return render_template("parameter/model_select_edit.html",select=select)

#修改模型值页面save
@app.route('/parameter/edit_select_save/<int:p_id>', methods=['POST'])
def edit_select_save(p_id):
	
	name = request.form["name"]
	score = request.form["score"]
	select = Rcs_Parameter_Select.query.filter_by(id=p_id).first()
	select.name = name
	select.score = score
	tree = Rcs_Parameter_Tree.query.filter_by(id=select.tree_id).first()
	try:
		db.session.commit()
		# 消息闪现
		flash('修改成功','success')
	except:
		# 回滚
		db.session.rollback()
		logger.exception('exception')
		# 消息闪现
		flash('修改失败','error')
	return redirect("/parameter/model_"+tree.param_type)

#修改模型值页面delete
@app.route('/parameter/edit_select_delete/<int:p_id>', methods=['POST'])
def edit_select_delete(p_id):
	select = Rcs_Parameter_Select.query.filter_by(id=p_id).first()
	tree = Rcs_Parameter_Tree.query.filter_by(id=select.tree_id).first()
	Rcs_Parameter_Select.query.filter_by(id=p_id).delete()
	try:
		db.session.commit()
		# 消息闪现
		flash('删除成功','success')
	except:
		# 回滚
		db.session.rollback()
		logger.exception('exception')
		# 消息闪现
		flash('删除失败','error')
	return redirect("/parameter/model_"+tree.param_type)

#判断是否存在子节点(不存在，删除)
@app.route('/parameter/autoChild/<int:p_id>', methods=['GET'])
def autoChild(p_id):
	tree = Rcs_Parameter_Tree.query.filter_by(pId=p_id).all()
	if tree:
		return "false"
	else:
		try:
			Rcs_Parameter_Tree.query.filter_by(id=p_id).delete()
			Rcs_Parameter_Select.query.filter_by(tree_id=p_id).delete()
			db.session.commit()
			# 消息闪现
			flash('删除成功','success')
		except:
			# 回滚
			db.session.rollback()
			logger.exception('exception')
			# 消息闪现
			flash('删除失败','error')
		return "true"

#同级下重名判断
@app.route('/parameter/doubleName/<int:p_id>/<operate_type>/<int:type>/<name>', methods=['GET'])
def doubleName(p_id,operate_type,type,name):
	#模型项
	if type==1:
		tree = Rcs_Parameter_Tree.query.filter_by(pId=p_id,name=name).all()
		for obj in tree:
			if name==obj.name:
				return helpers.show_result_success("")
		else:
			return helpers.show_result_fail("")
	#模型值
	else:
		select = Rcs_Parameter_Select.query.filter_by(tree_id=p_id).all()
		for obj in select:
			if name==obj.name:
				return helpers.show_result_success("")
		else:
			return helpers.show_result_fail("")