# coding:utf-8
import hashlib
import base64
from RemoteCreditSystem import User
from flask import request, render_template,flash,redirect
from flask.ext.login import login_user, logout_user, current_user, login_required
from RemoteCreditSystem import app
from RemoteCreditSystem import db
from RemoteCreditSystem.config import logger
from RemoteCreditSystem.config import PER_PAGE
import RemoteCreditSystem.helpers as helpers

from RemoteCreditSystem.models.system_usage.SC_Application_Lrb import SC_Application_Lrb
from RemoteCreditSystem.models.system_usage.SC_Application_Xjllb import SC_Application_Xjllb
from RemoteCreditSystem.models.system_usage.SC_Application_Zcfzb import SC_Application_Zcfzb

import RemoteCreditSystem.logic.xxlr.xxlr as xxlr

# 标准 资产负债表
@app.route('/xxlr/zcfzb_bz/<int:loan_apply_id>', methods=['GET'])
def xxlr_zcfzb_bz(loan_apply_id):
	sc_application_zcfzb = SC_Application_Zcfzb.query.filter_by(loan_apply_id=loan_apply_id).first()
	table_content = ''
	if(sc_application_zcfzb != None):
		table_content = base64.b64decode(sc_application_zcfzb.table_content).decode("utf-8")
	return render_template("xxlr/zcfzb_bz.html",loan_apply_id=loan_apply_id,sc_application_zcfzb=sc_application_zcfzb,table_content=table_content)

# 保存 标准 资产负债表
@app.route('/xxlr/zcfzb_bz/save.json/<int:loan_apply_id>', methods=['POST'])
def xxlr_zcfzb_bz_save(loan_apply_id):
	try:
		xxlr.xxlr_zcfzb_bz_save(loan_apply_id,request)
		# zcfzb = SC_Application_Zcfzb.query.filter_by(loan_apply_id=loan_apply_id).first()
		# if zcfzb:
		# 	zcfzb.table_content = score
		# else:
		# 	zcfzb = SC_Application_Zcfzb(loan_apply_id,score).add()
		# # 事务提交
		# db.session.commit()
		# 消息闪现
		flash('保存成功','success')
		return helpers.show_result_success("")
	except:
		logger.exception('exception')
		# 消息闪现
		flash('保存失败','error')
		return helpers.show_result_fail("")
	# return redirect("/xxlr/zcfzb_bz/"+str(loan_apply_id))

# 标准 利润表
@app.route('/xxlr/lrb_bz/<int:loan_apply_id>', methods=['GET'])
def xxlr_lrb_bz(loan_apply_id):
	sc_application_lrb = SC_Application_Lrb.query.filter_by(loan_apply_id=loan_apply_id).first()
	table_content = ''
	if(sc_application_lrb != None):
		table_content = base64.b64decode(sc_application_lrb.table_content).decode("utf-8")
	return render_template("xxlr/lrb_bz.html",loan_apply_id=loan_apply_id,sc_application_lrb=sc_application_lrb,table_content=table_content)

# 保存 标准 利润表
@app.route('/xxlr/lrb_bz/save.json/<int:loan_apply_id>/<value1>', methods=['POST'])
def xxlr_lrb_bz_save(loan_apply_id,value1):
	try:
		xxlr.xxlr_lrb_bz_save(loan_apply_id,request,value1)
		# 消息闪现
		flash('保存成功','success')
		return helpers.show_result_success("")
	except:
		logger.exception('exception')
		# 消息闪现
		flash('保存失败','error')
		return helpers.show_result_fail("")
   
# 标准 现金流量表
@app.route('/xxlr/xjllb_bz/<int:loan_apply_id>', methods=['GET'])
def xxlr_xjllb_bz(loan_apply_id):
	sc_application_xjllb = SC_Application_Xjllb.query.filter_by(loan_apply_id=loan_apply_id).first()
	table_content = ''
	if(sc_application_xjllb != None):
		table_content = base64.b64decode(sc_application_xjllb.table_content).decode("utf-8")
	return render_template("xxlr/xjllb_bz.html",loan_apply_id=loan_apply_id,sc_application_xjllb=sc_application_xjllb,table_content=table_content)

# 保存 标准 现金流量表
@app.route('/xxlr/xjllb_bz/save.json/<int:loan_apply_id>', methods=['POST'])
def xxlr_xjllb_bz_save(loan_apply_id):
	try:
		xxlr.xxlr_xjllb_bz_save(loan_apply_id,request)
		# 消息闪现
		flash('保存成功','success')
		return helpers.show_result_success("")
	except:
		logger.exception('exception')
		# 消息闪现
		flash('保存失败','error')
		return helpers.show_result_fail("")