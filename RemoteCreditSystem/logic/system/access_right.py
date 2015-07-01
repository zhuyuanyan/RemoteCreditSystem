#coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user

import json

from RemoteCreditSystem import db
from RemoteCreditSystem.models import Role,UserRole,Rcs_Access_Right
import RemoteCreditSystem.helpers as helpers
import RemoteCreditSystem.tools.xmlUtil as xmlUtil

#保存权限
def accessright_save_json(roleId,decodejson):
    try:
        #先删除该角色对应权限
        Rcs_Access_Right.query.filter_by(role_id=roleId).delete()
        db.session.flush()
        
        for obj in decodejson:
            if(obj['levels']=='1' or obj['levels']=='2'):
                Rcs_Access_Right(roleId,obj['id'],0).add()
            elif(obj['levels']=='3'):
                operations = 0
                for obj_c in obj['children']:
                    if(obj_c['checked']):
                        operations += int(obj_c['operations'],10)
                Rcs_Access_Right(roleId,obj['id'],operations).add()
                
        # 事务提交
        db.session.commit()
    except:
        # 回滚
        db.session.rollback()
        #抛出异常到view view负责打印
        raise
    
#页面按钮验证权限
def checkBtnPri(resource_id,pri_type):
    role_id = UserRole.query.filter_by(user_id=current_user.id).first().role_id
    access_right = Rcs_Access_Right.query.filter_by(resource_id=resource_id,role_id=role_id).first()
    if(access_right == None):
        return False
    else:
        if(access_right.operations & int(xmlUtil.getresource(pri_type)['code']) != 0):
            return True
        else:
            return False
