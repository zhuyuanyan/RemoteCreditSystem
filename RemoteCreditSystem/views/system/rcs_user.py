# coding:utf-8
from RemoteCreditSystem import db
from RemoteCreditSystem.config import PER_PAGE
from RemoteCreditSystem.config import logger
import RemoteCreditSystem.helpers as helpers
import datetime

from flask import Module, session, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user

from RemoteCreditSystem.models import User
from RemoteCreditSystem.models import Role
from RemoteCreditSystem.models import UserRole
from RemoteCreditSystem.models import Rcs_Menu
from RemoteCreditSystem.models import Rcs_Privilege


from RemoteCreditSystem import app

import hashlib

#get md5 of a input string  
def GetStringMD5(str):  
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest() 
	
# 使用者管理
@app.route('/System/user.page/<int:page>', methods=['GET'])
def System_user(page):
	users = User.query.order_by("id").paginate(page, per_page = PER_PAGE)
	return render_template("System/user/user.html",users=users)
	
# 新增用户
@app.route('/System/new_user.json', methods=['GET','POST'])
def new_user():
    if request.method == 'GET':
		roles = Role.query.order_by("id").all()
		return render_template("System/user/new_user.html",roles=roles)
    else:
        try:
            user = User(request.form['login_name'],GetStringMD5(request.form['login_password']),
                request.form['real_name'],request.form['sex'],request.form['mobile'],request.form['active'],request.form['email'],"","","","","","","","","")
            user.add()

            #清理缓存
            db.session.flush()
            
            UserRole(user.id,request.form['roles']).add()

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
    return redirect('System/user.page/1')

# 编辑用户
@app.route('/System/edit_user.json/<int:id>', methods=['GET','POST'])
def edit_user(id):
    if request.method == 'GET':
        user = User.query.filter_by(id=id).first()
        roles = Role.query.order_by("id").all()
        userrole = UserRole.query.filter_by(user_id=id).first()
        return render_template("System/user/edit_user.html",user=user,roles=roles,userrole=userrole)
    else:
        try:
            user = User.query.filter_by(id=id).first()
            user.login_name = request.form['login_name']
            #user.login_password = request.form['login_password']
            user.real_name = request.form['real_name']
            user.sex = request.form['sex']
            user.mobile = request.form['mobile']
            user.active = request.form['active']
            user.email = request.form['email']
            user.modify_user = current_user.id
            user.modify_date = datetime.datetime.now()

            user_role = UserRole.query.filter_by(user_id=id).first()
            user_role.role_id = request.form['roles']
            user_role.modify_user = current_user.id
            user_role.modify_date = datetime.datetime.now()

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
        return redirect('System/user.page/1')

# 禁用用户
@app.route('/System/disable_user.json/<type>/<int:id>', methods=['GET'])
def disable_user(type,id):
    try:
        user = User.query.filter_by(id=id).first()
        user.active = type
        
        # 事务提交
        db.session.commit()
        # 消息闪现
        return helpers.show_result_success('保存成功')
    except:
        # 回滚
        db.session.rollback()
        logger.exception('exception')
        return helpers.show_result_fail('保存失败')
    
    
# 角色权限管理
@app.route('/System/role.page/<int:page>', methods=['GET'])
def System_jsqxgl(page):
    # 获取角色并分页
    roles = Role.query.order_by("id").paginate(page, per_page = PER_PAGE)
    return render_template("System/role/role.html",roles = roles)

# 新增角色
@app.route('/System/new_role.json', methods=['GET','POST'])
def new_role():
    if request.method == 'POST':
        try:
            # 保存角色
            Role(request.form['role_name']).add()

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

        return redirect('System/role.page/1')

    elif request.method == 'GET':
        return render_template("System/role/new_role.html")

# 更新角色
@app.route('/System/edit_role.json/<int:id>', methods=['GET','POST'])
def edit_role(id):
    if request.method == 'POST':
        try:
            Role.query.filter_by(id=id).update({"role_name":request.form['role_name']})

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

        return redirect('System/role.page/1')

    elif request.method == 'GET':
        role = Role.query.filter_by(id=id).first()

        return render_template("System/role/edit_role.html",role=role)