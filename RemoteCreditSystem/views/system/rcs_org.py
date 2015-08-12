# coding:utf-8
from RemoteCreditSystem import db
from RemoteCreditSystem.config import PER_PAGE
from RemoteCreditSystem.config import logger
import RemoteCreditSystem.helpers as helpers
import datetime

from flask import Module, session, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user,login_required

from RemoteCreditSystem.models import User
from RemoteCreditSystem.models import Role
from RemoteCreditSystem.models import UserRole
from RemoteCreditSystem.models import Org

from RemoteCreditSystem import app
from RemoteCreditSystem import dynDict
import hashlib

import RemoteCreditSystem.tools.xmlUtil as xmlUtil
from RemoteCreditSystem.tools.DynDictCache import DynDictCache

# 机构管理
@app.route('/System/org.page', methods=['GET'])
@login_required
def System_org():
    orgs = Org.query.order_by("id")
    return render_template("System/org/org.html",orgs=orgs)
    
# 加载树
@app.route('/System/org/org.json', methods=['GET','POST'])
def init_org_tree():
    # 加载所有
    tree = Org.query.order_by("id").all()
    for obj in tree:
        obj.icon = "/static/img/icon_4.png"
    return helpers.show_result_content(tree) # 返回json

# 新增机构
@app.route('/System/new_org.page/<int:pId>', methods=['GET'])
def new_org_page(pId):
    return render_template("System/org/new_org.html",pId=pId)
    
# 新增机构
@app.route('/System/new_org.json/<int:pId>', methods=['POST'])
def new_org_json(pId):
    try:
        levels = Org.query.filter_by(id=pId).first().levels + 1
        Org(request.form['org_name'],pId,levels).add()
        
        # 事务提交
        db.session.commit()
        # 消息闪现
        flash('保存成功','success')
    except:
        # 回滚
        db.session.rollback()
        logger.exception('exception')
        # 消息闪现
        flash('保存失败','error')
    finally:
        xmlUtil.updateDynDict('org_all')
    return redirect('System/org.page')

# 编辑机构
@app.route('/System/edit_org.page/<int:id>', methods=['GET'])
def edit_org_page(id):
    org = Org.query.filter_by(id=id).first()
    return render_template("System/org/edit_org.html",org=org)

# 编辑机构
@app.route('/System/edit_org.json/<int:id>', methods=['POST'])
def edit_org_json(id):
    try:
        org = Org.query.filter_by(id=id).first()
        org.org_name = request.form['org_name']
        
        # 事务提交
        db.session.commit()
        # 消息闪现
        flash('保存成功','success')
    except:
        # 回滚
        db.session.rollback()
        logger.exception('exception')
        # 消息闪现
        flash('保存失败','error')
    finally:
        xmlUtil.updateDynDict('org_all')
    return redirect('System/org.page')
        
# 删除机构
@app.route('/System/delete_org.page/<int:id>', methods=['GET'])
def delete_org_page(id):
    org = Org.query.filter_by(id=id).first()
    return render_template("System/org/edit_org.html",org=org)