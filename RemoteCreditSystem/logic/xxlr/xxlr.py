#coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user

import datetime
import os

from RemoteCreditSystem import db
from RemoteCreditSystem.config import logger
from RemoteCreditSystem.models.system_usage.SC_Application_Lrb import SC_Application_Lrb
from RemoteCreditSystem.models.system_usage.SC_Application_Xjllb import SC_Application_Xjllb
from RemoteCreditSystem.models.system_usage.SC_Application_Zcfzb import SC_Application_Zcfzb
from RemoteCreditSystem.models.system_usage.Rcs_Application_Info import Rcs_Application_Info
from RemoteCreditSystem.models.system_usage.Rcs_Application_Score import Rcs_Application_Score
from RemoteCreditSystem.models.system_usage.Rcs_Parameter import Rcs_Parameter

def xxlr_zcfzb_bz_save(loan_apply_id,request):
    try:
        SC_Application_Zcfzb.query.filter_by(loan_apply_id=loan_apply_id).delete()
        db.session.flush()
        SC_Application_Zcfzb(loan_apply_id,request.form['content']).add()
        info = Rcs_Application_Info.query.filter_by(id=loan_apply_id).first()
        if info:
            #设置为标准模型
            info.model_type=2
        db.session.commit()
    except:
        # 回滚
        db.session.rollback()
        #抛出异常到view view负责打印
        raise
    
def xxlr_lrb_bz_save(loan_apply_id,request,value1):
    try:
        SC_Application_Lrb.query.filter_by(loan_apply_id=loan_apply_id).delete()
        db.session.flush()
        
        SC_Application_Lrb(loan_apply_id,request.form['content']).add()
        #月利润
        pet = value1
        info = Rcs_Application_Info.query.filter_by(id=loan_apply_id).first()
        if info:
            #设置为标准模型
            info.model_type=2
        #获取还款能力参数配置数据
        parm = Rcs_Parameter.query.filter_by(parameter_name='hknl').first()
        if parm:
            print "----------2"
            value = parm.parameter_value.split(',')
            value = value[140]
            #获取标准还款能力数据
            score = Rcs_Application_Score.query.filter_by(application_id=loan_apply_id).first()
            print "-------1"
            print value
            print pet
            if score:
                score.hknl_score = float(value)*float(pet)
            else:
                print "----------------"
                Rcs_Application_Score(loan_apply_id,'',float(value)*float(pet),'','','','').add()

        db.session.commit()
    except:
        # 回滚
        db.session.rollback()
        #抛出异常到view view负责打印
        raise
    
def xxlr_xjllb_bz_save(loan_apply_id,request):
    try:
        SC_Application_Xjllb.query.filter_by(loan_apply_id=loan_apply_id).delete()
        db.session.flush()
        
        SC_Application_Xjllb(loan_apply_id,request.form['content']).add()
        info = Rcs_Application_Info.query.filter_by(id=loan_apply_id).first()
        if info:
            #设置为标准模型
            info.model_type=2
        db.session.commit()
    except:
        # 回滚
        db.session.rollback()
        #抛出异常到view view负责打印
        raise