# coding:utf-8
from RemoteCreditSystem import db
from RemoteCreditSystem.config import logger
import RemoteCreditSystem.helpers as helpers
import datetime

from flask import Module, session, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user

from RemoteCreditSystem.models import Rcs_Menu

from RemoteCreditSystem import app

# 模块管理
@app.route('/System/menu', methods=['GET'])
def System_menu():
    return render_template("System/menu/menu.html")

# 加载树
@app.route('/System/tree/menu/<int:id>', methods=['GET','POST'])
def init_access_tree(id):
    # 加载所有
    if id == 0:
        tree = Rcs_Menu.query.order_by("id").all()
    else:
        tree = Rcs_Menu.query.filter_by(pid=id).order_by("id").all()
        
    return helpers.show_result_content(tree) # 返回json

# 新增模块或菜单
@app.route('/System/new_menu/<int:pId>', methods=['GET','POST'])
def new_menu(pId):
    if request.method == 'POST':
        try:
            menu = Rcs_Menu.query.filter_by(id=pId).first()
            Rcs_Menu(request.form['name'],request.form['menu_code'],pId,menu.level+1).add()

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

        return redirect('System/menu')
    else:
        return render_template("System/menu/new_menu.html",pId=pId)

# 编辑模块或菜单
@app.route('/System/edit_menu/<int:id>', methods=['GET','POST'])
def edit_menu(id):
    if request.method == 'POST':
        try:
            obj = Rcs_Menu.query.filter_by(id=id).first()
            obj.name = request.form['name']
            obj.menu_code = request.form['menu_code']

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

        return redirect('System/menu')
    else:
        obj = Rcs_Menu.query.filter_by(id=id).first()
        return render_template("System/menu/edit_menu.html",obj=obj)
            
# 删除模块或菜单
@app.route('/System/delete_menu/<int:id>', methods=['GET','POST'])
def delete_menu(id):
    try:
        Rcs_Menu.query.filter_by(id=id).delete()

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

    return redirect('System/menu')