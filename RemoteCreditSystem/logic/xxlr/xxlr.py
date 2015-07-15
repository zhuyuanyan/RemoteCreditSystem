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

def xxlr_zcfzb_bz_save(loan_apply_id,request):
    try:
        SC_Application_Zcfzb.query.filter_by(loan_apply_id=loan_apply_id).delete()
        db.session.flush()
        SC_Application_Zcfzb(loan_apply_id,request.form['content']).add()
        
        db.session.commit()
    except:
        # 回滚
        db.session.rollback()
        #抛出异常到view view负责打印
        raise
    
def xxlr_lrb_bz_save(loan_apply_id,request):
    try:
        SC_Application_Lrb.query.filter_by(loan_apply_id=loan_apply_id).delete()
        db.session.flush()
        
        SC_Application_Lrb(loan_apply_id,request.form['content']).add()
        
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
        
        db.session.commit()
    except:
        # 回滚
        db.session.rollback()
        #抛出异常到view view负责打印
        raise