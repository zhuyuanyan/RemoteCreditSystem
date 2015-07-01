# coding:utf-8
from RemoteCreditSystem import db
from RemoteCreditSystem.config import logger
import RemoteCreditSystem.helpers as helpers
import datetime
import json

from flask import Module, session, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user

from RemoteCreditSystem.models import Role
from RemoteCreditSystem.models import Rcs_Access_Right

from RemoteCreditSystem import app
from RemoteCreditSystem.tools.SimpleCache import SimpleCache

import RemoteCreditSystem.logic.system.access_right as access_right

# 模块管理
@app.route('/System/menu.page', methods=['GET'])
def menu_page():
    return render_template("System/menu/menu.html")

# 加载菜单树
@app.route('/System/menu/tree.json/<int:roleId>', methods=['POST'])
def menu_tree_json(roleId):
    simplecache = SimpleCache.getInstance()
    tree = [] 
    #未点击角色
    if(roleId == 0):
        for key_cache in simplecache:  
            obj_tmp = simplecache[key_cache]  
            obj_tmp['checked'] = False        
            tree.append(obj_tmp)
    #点击角色
    else:
        rcs_access_right = Rcs_Access_Right.query.filter_by(role_id=roleId).order_by("id").all()
        for key_cache in simplecache:  
            obj_tmp = simplecache[key_cache]
            obj_tmp['checked'] = False
            for obj_access_right in rcs_access_right:
                if(obj_tmp['levels'] != '4'): 
                    if(obj_tmp['id'] == obj_access_right.resource_id):
                        obj_tmp['checked'] = True
                        break;  
                elif(obj_tmp['levels'] == '4'):
                    if(obj_tmp['id'].split("_")[0] == obj_access_right.resource_id):
                        if(int(obj_access_right.operations) & int(obj_tmp['id'].split("_")[1]) != 0):
                            obj_tmp['checked'] = True
                        break; 
            tree.append(obj_tmp)
    return helpers.show_result_content(tree) # 返回json

#加载角色树
@app.route('/System/role/tree.json', methods=['POST'])
def role_tree_json():
    tree = Role.query.order_by("id").all()
    return helpers.show_result_content(tree) # 返回json

#保存权限
@app.route('/System/accessright/save.json/<int:roleId>', methods=['POST'])
def accessright_save_json(roleId):
    try:
        decodejson = json.loads(request.form['nodesJsonStr'])
        access_right.accessright_save_json(roleId, decodejson)
        # 消息闪现
        flash('保存成功','success')
        return helpers.show_result_success('') # 返回json
    except:
        logger.exception('exception')
        # 消息闪现
        flash('保存失败','error')
        return helpers.show_result_fail('') # 返回json
