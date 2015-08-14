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
from RemoteCreditSystem.models.system_usage.Rcs_Expert_Information import Rcs_Expert_Information

from RemoteCreditSystem import app
import RemoteCreditSystem.tools.xmlUtil as xmlUtil
import hashlib

#get md5 of a input string  
def GetStringMD5(str):  
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest() 

# 使用者管理
@app.route('/System/user.page/<int:page>', methods=['GET'])
@login_required
def System_user(page):
    #users = User.query.order_by("id").paginate(page, per_page = PER_PAGE)
    return render_template("System/user/user.html")

# 加载树
@app.route('/System/org_user/org_user.json', methods=['GET','POST'])
def init_org_user_tree():
    # 加载所有
    tree = Org.query.order_by("id").all()
    for obj in tree:
        obj.id = "org_"+str(obj.id)
        obj.type = "org"
        obj.pId = "org_"+str(obj.pId)
        obj.icon = "/static/img/icon_4.png"
    
    #admin用户屏蔽
    users = User.query.filter("id !=1").order_by("id").all()
    for obj in users:
        tmp = Org(obj.real_name,obj.org_id,None)
        tmp.id = "user_"+str(obj.id)
        tmp.type = "user"
        tmp.sex = obj.sex
        tmp.active = obj.active
        tmp.login_name = obj.login_name
        tmp.real_name = obj.real_name
        tmp.pId = "org_1"
        if(obj.org_id is not None):
            tmp.pId = "org_"+str(obj.org_id)
        elif(obj.pId is not None):
            tmp.pId = "user_"+str(obj.pId)
            
        tmp.icon = "/static/img/icon_5.png"
        tree.append(tmp)
    
    return helpers.show_result_content(tree) # 返回json

# 新增用户
@app.route('/System/new_user.json/<pId>', methods=['GET','POST'])
def new_user(pId):
    if request.method == 'GET':
        roles = Role.query.order_by("id").all()
        return render_template("System/user/new_user.html",roles=roles,pId=pId)
    else:
        try:
            chk = User.query.filter_by(login_name=request.form['login_name']).all()
            if(chk):
                # 消息闪现
                flash('保存失败，登录名重复','error')
                return redirect('System/user.page/1')
            level = request.form['level']
            if('user' in pId):
                user = User(request.form['login_name'],GetStringMD5(request.form['login_password']),
                    request.form['real_name'],request.form['sex'],request.form['mobile'],request.form['active'],request.form['email'],request.form['card_id'],level,
                    None,int(pId.split("_")[1]))
                user.add()
            else:
                user = User(request.form['login_name'],GetStringMD5(request.form['login_password']),
                    request.form['real_name'],request.form['sex'],request.form['mobile'],request.form['active'],request.form['email'],request.form['card_id'],level,
                    int(pId.split("_")[1]),None)
                user.add()

            #清理缓存
            db.session.flush()
            UserRole(user.id,request.form['roles']).add()

            
            # 专家
            if level!='3':
                #专家信息
                address = request.form['address']
                hy = request.form['hy']
                qy = request.form['qy']
                product = request.form['product']
                balance = request.form['balance']
                zyzc = request.form['zyzc']
                xrzw = request.form['xrzw']
                expert_level = request.form['expert_level']
                approve_role = request.form['approve_role']
                gzr = request.form['gzr']
                gzsd = request.form['gzsd']
                Rcs_Expert_Information(user.id,address,hy,qy,product,balance,zyzc,xrzw,expert_level,approve_role,gzr,gzsd).add() 
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
            xmlUtil.updateDynDict('user_all')
    return redirect('System/user.page/1')

# 编辑用户
@app.route('/System/edit_user.json/<int:id>', methods=['GET','POST'])
def edit_user(id):
    if request.method == 'GET':
        user = User.query.filter_by(id=id).first()
        roles = Role.query.order_by("id").all()
        userrole = UserRole.query.filter_by(user_id=id).first()
        user_info = Rcs_Expert_Information.query.filter_by(expert_id=id).first()
        return render_template("System/user/edit_user.html",user=user,roles=roles,userrole=userrole,user_info=user_info)
    else:
        try:
            level = request.form['level']
            chk = User.query.filter("login_name='"+request.form['login_name']+"' and id != "+str(id)).all()
            if(chk):
                # 消息闪现
                flash('保存失败，登录名重复','error')
                return redirect('System/user.page/1')
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
            if level!='3':
                user_info = Rcs_Expert_Information.query.filter_by(expert_id=id).first()
                address = request.form['address']
                hy = request.form['hy']
                qy = request.form['qy']
                product = request.form['product']
                balance = request.form['balance']
                zyzc = request.form['zyzc']
                xrzw = request.form['xrzw']
                expert_level = request.form['expert_level']
                approve_role = request.form['approve_role']
                gzr = request.form['gzr']
                gzsd = request.form['gzsd']
                if user_info:
                    user_info.address=address
                    user_info.hy=hy
                    user_info.qy=qy
                    user_info.product=product
                    user_info.balance=balance
                    user_info.zyzc=zyzc
                    user_info.xrzw=xrzw
                    user_info.expert_level=expert_level
                    user_info.approve_role=approve_role
                    user_info.gzr=gzr
                    user_info.gzsd=gzsd
            user_role = UserRole.query.filter_by(user_id=id).first()
            if user_role:
                user_role.role_id = request.form['roles']
            else:
                UserRole(id,request.form['roles']).add()

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
            xmlUtil.updateDynDict('user_all')
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
        flash('保存成功','success')
        return helpers.show_result_success('保存成功')
    except:
        # 回滚
        db.session.rollback()
        logger.exception('exception')
        # 消息闪现
        flash('保存失败','error')
        return helpers.show_result_fail('保存失败')
    finally:
        xmlUtil.updateDynDict('user_all')
    
    
# 角色权限管理
@app.route('/System/role.page/<int:page>', methods=['GET'])
@login_required
def System_jsqxgl(page):
    # 获取角色并分页
    roles = Role.query.order_by("id").paginate(page, per_page = PER_PAGE)
    return render_template("System/role/role.html",roles = roles)

# 新增角色
@app.route('/System/new_role.json', methods=['GET','POST'])
def new_role():
    if request.method == 'POST':
        try:
            chk = Role.query.filter_by(role_name=request.form['role_name']).all()
            if(chk):
                # 消息闪现
                flash('保存失败，角色名重复','error')
                return redirect('System/role.page/1')
            
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
        finally:
            xmlUtil.updateDynDict('role_all')

        return redirect('System/role.page/1')

    elif request.method == 'GET':
        return render_template("System/role/new_role.html")

# 更新角色
@app.route('/System/edit_role.json/<int:id>', methods=['GET','POST'])
def edit_role(id):
    if request.method == 'POST':
        try:
            chk = Role.query.filter("role_name='"+request.form['role_name']+"' and id<>"+str(id)).all()
            if(chk):
                # 消息闪现
                flash('保存失败，角色名重复','error')
                return redirect('System/role.page/1')
            
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
        finally:
            xmlUtil.updateDynDict('role_all')

        return redirect('System/role.page/1')

    elif request.method == 'GET':
        role = Role.query.filter_by(id=id).first()

        return render_template("System/role/edit_role.html",role=role)
    
# 移动到用户
@app.route('/System/user/change_belong_user', methods=['GET','POST'])
def change_belong_user():
    try:
        user = User.query.filter_by(id=request.form['user_id']).first()
        user.org_id = None
        user.pId = request.form['belong_user']
        
        sql = "FIND_IN_SET(id ,getUserList('"+request.form['user_id']+"'))"
        users = User.query.filter(sql).order_by("id").all()
        for obj in users:
            if str(obj.id) == request.form['belong_user']:#环状结构 不允许
                # 消息闪现
                flash('保存失败 不允许环状结构! ','error')
                return render_template("System/user/user.html")
            
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
    
    return render_template("System/user/user.html")

# 移动到机构
@app.route('/System/user/change_belong_org', methods=['GET','POST'])
def change_belong_org():
    try:
        user = User.query.filter_by(id=request.form['user_id']).first()
        user.pId = None
        user.org_id = request.form['belong_org']
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
    return render_template("System/user/user.html")

# 删除角色
@app.route('/System/delete_role/<int:id>', methods=['GET'])
def delete_role(id):
    try:
        UserRole.query.filter_by(role_id=id).delete()
        Role.query.filter_by(id=id).delete()
        
        # 事务提交
        db.session.commit()
        # 消息闪现
        flash('删除成功','success')
    except:
        # 回滚
        db.session.rollback()
        logger.exception('exception')
        # 消息闪现
        flash('删除失败','error')
    finally:
        xmlUtil.updateDynDict('role_all')
    return ''