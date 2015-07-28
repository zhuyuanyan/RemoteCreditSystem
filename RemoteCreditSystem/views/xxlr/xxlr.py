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
from RemoteCreditSystem.models.system_usage.SC_Application_Syb import SC_Application_Syb
from RemoteCreditSystem.models.system_usage.SC_Application_Hknl import SC_Application_Hknl

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

		return helpers.show_result_success("")
	except:
		logger.exception('exception')
	
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

		return helpers.show_result_success("")
	except:
		logger.exception('exception')
	
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
	
		return helpers.show_result_success("")
	except:
		logger.exception('exception')
		
		return helpers.show_result_fail("")
	
# 标准 损益表
@app.route('/xxlr/syb_bz/<int:loan_apply_id>', methods=['GET'])
def xxlr_syb_bz(loan_apply_id):
	sc_application_syb = SC_Application_Syb.query.filter_by(loan_apply_id=loan_apply_id).first()
	table_content = ''
	if(sc_application_syb != None):
		table_content = base64.b64decode(sc_application_syb.table_content).decode("utf-8")
	return render_template("xxlr/syb_bz.html",loan_apply_id=loan_apply_id,sc_application_syb=sc_application_syb,table_content=table_content)

# 保存 标准 损益表
@app.route('/xxlr/syb_bz/save.json/<int:loan_apply_id>', methods=['POST'])
def xxlr_syb_bz_save(loan_apply_id):
	try:
		xxlr.xxlr_syb_bz_save(loan_apply_id,request)
		
		return helpers.show_result_success("")
	except:
		logger.exception('exception')
	
		return helpers.show_result_fail("")
	
# 标准 还款能力
@app.route('/xxlr/hknl_bz/<int:loan_apply_id>', methods=['GET'])
def xxlr_hknl_bz(loan_apply_id):
	try:
		xxlr.compute_hknl_bz(loan_apply_id)
	except:
		logger.exception('exception')
		
	sc_application_hknl = SC_Application_Hknl.query.filter_by(loan_apply_id=loan_apply_id).first()
	#取出还款能力旧数据
	form_data = {}
	if(sc_application_hknl):
		tmp = sc_application_hknl.form_data
		for key_value in tmp.split('&'):
			form_data[key_value.split("=")[0]]=key_value.split("=")[1]
	return render_template("xxlr/hknl_bz.html",loan_apply_id=loan_apply_id,form_data=form_data)