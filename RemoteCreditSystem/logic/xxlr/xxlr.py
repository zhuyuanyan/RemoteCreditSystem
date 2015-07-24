#coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user

import datetime
import os
import string

from RemoteCreditSystem import db
from RemoteCreditSystem.config import logger
from RemoteCreditSystem.models.system_usage.SC_Application_Lrb import SC_Application_Lrb
from RemoteCreditSystem.models.system_usage.SC_Application_Xjllb import SC_Application_Xjllb
from RemoteCreditSystem.models.system_usage.SC_Application_Zcfzb import SC_Application_Zcfzb
from RemoteCreditSystem.models.system_usage.SC_Application_Syb import SC_Application_Syb
from RemoteCreditSystem.models.system_usage.SC_Application_Hknl import SC_Application_Hknl
from RemoteCreditSystem.models.system_usage.Rcs_Application_Info import Rcs_Application_Info
from RemoteCreditSystem.models.system_usage.Rcs_Application_Score import Rcs_Application_Score
from RemoteCreditSystem.models.system_usage.Rcs_Parameter import Rcs_Parameter

def xxlr_zcfzb_bz_save(loan_apply_id,request):
    try:
        SC_Application_Zcfzb.query.filter_by(loan_apply_id=loan_apply_id).delete()
        db.session.flush()
        form_data = request.form['form_data']
        SC_Application_Zcfzb(loan_apply_id,request.form['content'],request.form['form_data']).add()
        db.session.flush()
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
        SC_Application_Lrb(loan_apply_id,request.form['content'],request.form['form_data']).add()
        db.session.flush()
        #月利润
        pet = value1
        info = Rcs_Application_Info.query.filter_by(id=loan_apply_id).first()
        if info:
            #设置为标准模型
            info.model_type=2
        #获取还款能力参数配置数据
        parm = Rcs_Parameter.query.filter_by(parameter_name='hknl').first()
        if parm:
            value = parm.parameter_value.split(',')
            value = value[140]
            #获取标准还款能力数据
            score = Rcs_Application_Score.query.filter_by(application_id=loan_apply_id).first()
            if score:
                score.hknl_score = float(value)*float(pet)
            else:
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
        SC_Application_Xjllb(loan_apply_id,request.form['content'],request.form['form_data']).add()
        db.session.flush()
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
    
def xxlr_syb_bz_save(loan_apply_id,request):
    try:
        SC_Application_Syb.query.filter_by(loan_apply_id=loan_apply_id).delete()
        db.session.flush()
        SC_Application_Syb(loan_apply_id,request.form['content'],request.form['form_data']).add()
        db.session.flush()
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
    
#计算还款能力
def compute_hknl_bz(loan_apply_id):
    try:
        sc_application_zcfzb = SC_Application_Zcfzb.query.filter_by(loan_apply_id=loan_apply_id).first()
        sc_application_lrb = SC_Application_Lrb.query.filter_by(loan_apply_id=loan_apply_id).first()
        sc_application_xjllb = SC_Application_Xjllb.query.filter_by(loan_apply_id=loan_apply_id).first()
        sc_application_syb = SC_Application_Syb.query.filter_by(loan_apply_id=loan_apply_id).first()
        
        sc_application_hknl = SC_Application_Hknl.query.filter_by(loan_apply_id=loan_apply_id).first()
        #取出还款能力旧数据
        form_data = {}
        if(sc_application_hknl):
            tmp = sc_application_hknl.form_data
            for key_value in tmp.split('&'):
                form_data[key_value.split("=")[0]]=key_value.split("=")[1]
                
        if(sc_application_zcfzb):
            zcfzb_form_data = sc_application_zcfzb.form_data
            #解析资负信息
            tmp_zcfzb={}
            for key_value in zcfzb_form_data.split('&'):
                tmp_zcfzb[key_value.split("=")[0]]=key_value.split("=")[1]
            
        if(sc_application_lrb):
            lrb_form_data = sc_application_lrb.form_data
            #解析利润表信息
            tmp_lrb={}
            for key_value in lrb_form_data.split('&'):
                tmp_lrb[key_value.split("=")[0]]=key_value.split("=")[1]
            
        if(sc_application_xjllb):
            xjllb_form_data = sc_application_xjllb.form_data
            #解析现金流信息
            tmp_xjllb={}
            for key_value in xjllb_form_data.split('&'):
                tmp_xjllb[key_value.split("=")[0]]=key_value.split("=")[1]
            
        if(sc_application_syb):
            syb_form_data = sc_application_syb.form_data
            #解析损益表信息
            tmp_syb={}
            for key_value in syb_form_data.split('&'):
                tmp_syb[key_value.split("=")[0]]=key_value.split("=")[1]
            
        #计算
        if float(tmp_zcfzb['F18'])==0:
            form_data['B1_1']=0
        else:
            form_data['B1_1']='%.2f' % (string.atof(tmp_zcfzb['C18'])/string.atof(tmp_zcfzb['F18']))
        if float(tmp_zcfzb['F18'])==0:
            form_data['B1_2']=0
        else:
            form_data['B1_2']='%.2f' % ((string.atof(tmp_zcfzb['C18'])-string.atof(tmp_zcfzb['C14']))/string.atof(tmp_zcfzb['F18']))
        if float(tmp_zcfzb['C41'])==0:
            form_data['B2_1']=0
        else:
            form_data['B2_1']='%.2f' % (string.atof(tmp_zcfzb['F28'])/string.atof(tmp_zcfzb['C41']))
        if float(tmp_zcfzb['C15'])==0:
            form_data['B2_6']=0
        else:
            form_data['B2_6']='%.2f' % (string.atof(tmp_zcfzb['F28'])/string.atof(tmp_xjllb['C15']))
        if float(tmp_zcfzb['B14'])==0 and float(tmp_zcfzb['C14'])==0:
            form_data['B3_1']=0
        else:
            form_data['B3_1']='%.2f' % (string.atof(tmp_lrb['E8'])/((string.atof(tmp_zcfzb['B14'])+string.atof(tmp_zcfzb['C14']))*2))
        if float(tmp_zcfzb['B9'])==0 and float(tmp_zcfzb['C9'])==0:
            form_data['B3_2']=0
        else:
            form_data['B3_2']='%.2f' % (string.atof(tmp_zcfzb['C9'])/((string.atof(tmp_zcfzb['B9'])+string.atof(tmp_zcfzb['C9']))*2))
        if float(tmp_zcfzb['B18'])==0 and float(tmp_zcfzb['C18'])==0:
            form_data['B3_3']=0
        else:
            form_data['B3_3']='%.2f' % (string.atof(tmp_lrb['E7'])/((string.atof(tmp_zcfzb['B18'])+string.atof(tmp_zcfzb['C18']))*2))
        if float(tmp_zcfzb['B25'])==0 and float(tmp_zcfzb['C25'])==0:
            form_data['B3_4']=0
        else:
            form_data['B3_4']='%.2f' % (string.atof(tmp_lrb['E7'])/((string.atof(tmp_zcfzb['B25'])+string.atof(tmp_zcfzb['C25']))*2))
        if float(tmp_zcfzb['B41'])==0 and float(tmp_zcfzb['C41'])==0:
            form_data['B3_5']=0
        else:
            form_data['B3_5']='%.2f' % (string.atof(tmp_lrb['E7'])/((string.atof(tmp_zcfzb['B41'])+string.atof(tmp_zcfzb['C41']))*2))
        if float(tmp_zcfzb['B41'])==0 and float(tmp_zcfzb['C41'])==0:
            form_data['B4_1']=0
        else:    
            form_data['B4_1']='%.2f' % (string.atof(tmp_lrb['E22'])/((string.atof(tmp_zcfzb['B41'])+string.atof(tmp_zcfzb['C41']))*2))
        if float(tmp_lrb['E7'])==0:
            form_data['B4_1']=0
            form_data['B4_6']=0
        else:
            form_data['B4_']='%.2f' % ((string.atof(tmp_lrb['E7'])-string.atof(tmp_lrb['E8']))/string.atof(tmp_lrb['E7']))
            form_data['B4_6']='%.2f' % (string.atof(tmp_lrb['E22'])/string.atof(tmp_lrb['E7']))
        res = ''
        #保存计算后的form_data
        for d,x in form_data.items():
            res += str(d)+"="+str(x)+"&"
        if(sc_application_hknl):
            if(res):
                sc_application_hknl.form_data = res[0:len(res)-1]
        else:
            if(res != ''):
                SC_Application_Hknl(loan_apply_id,res[0:len(res)-1]).add()
        
        db.session.commit()
    except:
        # 回滚
        db.session.rollback()
        #抛出异常到view view负责打印
        raise
    