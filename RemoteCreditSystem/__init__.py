#!/usr/bin/env python
#coding=utf-8
import sys
import os

_HERE = os.path.dirname(__file__)

reload(sys)  
sys.setdefaultencoding('utf8')

from flask import Flask, render_template,flash,session
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy #建立单app -johnny
#import ibm_db_sa.ibm_db_sa

from RemoteCreditSystem.tools.StaticDictCache import StaticDictCache
from RemoteCreditSystem.tools.DynDictCache import DynDictCache

# 初始化
app = Flask(__name__)

#过期时间20分钟
from datetime import timedelta
app.permanent_session_lifetime = timedelta(minutes=20)

# 读取配置文件
#app.config.from_object('RemoteCreditSystem.config.DevConfig') # sqlite
app.config.from_object('RemoteCreditSystem.config.ProConfig') # mysql

# 初始化数据库
db = SQLAlchemy(app)

# flask-login---start
from RemoteCreditSystem.models import User

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.unauthorized_handler
def unauthorized():
	# 消息闪现
    flash('请重新登录','error')
    return render_template("login.html")

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
# flask-login---end

# 404错误跳转
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', error = error), 404
	
# 500错误跳转
@app.errorhandler(500)
def page_not_found(error):
    return render_template('errors/500.html', error = error), 500
    
#读取xml
import tools.xmlUtil as xmlUtil
xmlUtil.readMenuXml(os.path.join(_HERE, 'menus.xml'))
xmlUtil.readStaticDictXml(os.path.join(_HERE, 'static-dictionary.xml'))
xmlUtil.readDynDictXml(os.path.join(_HERE, 'dynamic-dictionary.xml'))

#select展示
def dict(dictName,selectValue,selectText):
	staticdictcache = StaticDictCache.getInstance()
	return staticdictcache.getDict(dictName,selectValue,selectText)
app.jinja_env.filters['dict'] = dict

def dynDict(dictName,selectValue,selectText):
	dyndictcache = DynDictCache.getInstance()
	return dyndictcache.getDict(dictName,selectValue,selectText)
app.jinja_env.filters['dynDict'] = dynDict

#例
#<select>
#	<script>document.write(js.lang.String.decodeHtml('{{"123"|dict("","")}}'))</script>
#</select>

#页面按钮验证权限
import logic.system.access_right as access_right
def checkBtnPri(resource_id,pri_type):
    return access_right.checkBtnPri(resource_id,pri_type)
app.jinja_env.filters['checkBtnPri'] = checkBtnPri
#例
#{%- if '030010'|checkBtnPri('create') %}
#    <input id="id_save_button" type="button" class="btn btn-info" value="导入"/>
#{%- endif %}


# #启动java虚拟机
# from jpype import *
# jarpath = os.path.join(_HERE, 'ext_class/ReadExcel.jar')
# jvmArg = "-Djava.class.path=" + jarpath
# startJVM(getDefaultJVMPath(),"-ea",jvmArg)
# # shutdownJVM()

#---------------------------------
#加载试图--johnny 放在最后防止循环引用
#---------------------------------
import views.index
import views.system.rcs_user
import views.system.rcs_menu
import views.system.rcs_org

import views.process.dqdc

import views.mxpg.pldr
import views.xxlr.xxlr

import views.parameter.rcs_parameter
import views.customer.customer

import views.accessLog.access_log





