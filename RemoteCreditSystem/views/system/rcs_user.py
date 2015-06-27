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
@app.route('/System/user/<int:page>', methods=['GET'])
def System_user(page):
	users = User.query.order_by("id").paginate(page, per_page = PER_PAGE)
	return render_template("System/user/user.html",users=users)
	
# 新增用户
@app.route('/System/new_user', methods=['GET','POST'])
def new_user():
    if request.method == 'GET':
		roles = Role.query.order_by("id").all()
		return render_template("System/user/new_user.html",roles=roles)
    else:
        try:
            user = User(request.form['login_name'],GetStringMD5(request.form['login_password']),
                request.form['real_name'],request.form['sex'],request.form['mobile'],request.form['active'],request.form['email'])
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
    return redirect('System/user/1')

# 编辑用户
@app.route('/System/edit_user/<int:id>', methods=['GET','POST'])
def edit_user(id):
    if request.method == 'GET':
        user = User.query.filter_by(id=id).first()
        roles = Role.query.order_by("id").all()
        role = UserRole.query.filter_by(user_id=id).first().rcs_userrole_ibfk_2
        return render_template("System/user/edit_user.html",user=user,roles=roles,role=role)
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
        return redirect('System/user/1')

# 禁用用户
@app.route('/System/disable_user/<type>/<int:id>', methods=['GET'])
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
@app.route('/System/jsqxgl/<int:page>', methods=['GET'])
def System_jsqxgl(page):
    # 获取角色并分页
    roles = Role.query.order_by("id").paginate(page, per_page = PER_PAGE)
    return render_template("System/role/jsqxgl.html",roles = roles)

# 新增角色
@app.route('/System/new_role', methods=['GET','POST'])
def new_role():
    if request.method == 'POST':
        try:
            # 保存角色
            role = Role(request.form['role_name'], request.form['role_level'])
            role.add()
            # 清理缓存 以获得role的对象的id
            db.session.flush()

            # 保存具体权限
            menu_tree = Rcs_Menu.query.filter("level>0").order_by("id").all()
            for menu in menu_tree:
                Rcs_Privilege('SC_Role',role.id,'Rcs_Menu',menu.menu_code,request.form[menu.menu_code]).add()

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

        return redirect('System/jsqxgl/1')

    elif request.method == 'GET':
        #读取所有模块
        data = []
        app_tree = Rcs_Menu.query.filter_by(level=1).order_by("id").all()
        for app in app_tree:
            dic = {}
            dic['id'] = app.id
            dic['name'] = app.name
            dic['menu_code'] = app.menu_code
            app_children = []
            menu_tree = Rcs_Menu.query.filter_by(pId=app.id).order_by("id").all()
            for menu in menu_tree:
                app_children.append({'id':menu.id,'name':menu.name,'menu_code':menu.menu_code})
            dic['children'] = app_children
            data.append(dic)
        return render_template("System/role/new_role.html",data=data)

# 更新角色
@app.route('/System/edit_role/<int:id>', methods=['GET','POST'])
def edit_role(id):
    if request.method == 'POST':
        try:
            Role.query.filter_by(id=id).update({"role_name":request.form['role_name'],"role_level":request.form['role_level']})

            # 更新权限
            Rcs_Privilege.query.filter_by(privilege_master='SC_Role',privilege_master_id=id).delete()
            db.session.flush()

            # 保存具体权限
            menu_tree = Rcs_Menu.query.filter("level>0").order_by("id").all()
            for menu in menu_tree:
                Rcs_Privilege('SC_Role',id,'Rcs_Menu',menu.menu_code,request.form[menu.menu_code]).add()

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

        return redirect('System/jsqxgl/1')

    elif request.method == 'GET':
        role = Role.query.filter_by(id=id).first()
        
        #读取所有模块
        data = []
        app_tree = Rcs_Menu.query.filter_by(level=1).order_by("id").all()
        for app in app_tree:
            dic = {}
            dic['id'] = app.id
            dic['name'] = app.name
            dic['menu_code'] = app.menu_code
            app_children = []
            menu_tree = Rcs_Menu.query.filter_by(pId=app.id).order_by("id").all()
            for menu in menu_tree:
                app_children.append({'id':menu.id,'name':menu.name,'menu_code':menu.menu_code})
            dic['children'] = app_children
            data.append(dic)
        #获取该role的所有权限
        privileges_menu = Rcs_Privilege.query.filter_by(privilege_master='SC_Role',privilege_access='Rcs_Menu',
            privilege_master_id=id).order_by("id").all()

        return render_template("System/role/edit_role.html",role=role,data=data,privileges_menu=privileges_menu)