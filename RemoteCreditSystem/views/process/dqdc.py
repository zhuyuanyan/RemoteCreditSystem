# coding:utf-8
from RemoteCreditSystem import db
from RemoteCreditSystem.config import logger
import RemoteCreditSystem.helpers as helpers
import datetime
import base64

from flask import Module, session, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user

from RemoteCreditSystem import app

from RemoteCreditSystem.models.system_usage.Rcs_Application_Advice import Rcs_Application_Advice
from RemoteCreditSystem.models.system_usage.Rcs_Application_Expert import Rcs_Application_Expert
from RemoteCreditSystem.models.system_usage.Rcs_Application_Info import Rcs_Application_Info
from RemoteCreditSystem.models.credit_data.sc_excel_table_content import SC_Excel_Table_Content
from RemoteCreditSystem.models import Rcs_Application_Log

# 贷款调查——小额贷款
@app.route('/Process/dqdc/dqdc_xed/<int:id>', methods=['GET'])
def dqdc_xed(id):
    info = Rcs_Application_Info.query.filter_by(id=id).first()
    sc_excel_table_contents = SC_Excel_Table_Content.query.filter_by(loan_apply_id=id).order_by("sheet_type").all()
    return render_template("process/dqdc/dqdc_xed.html",info=info,sc_excel_table_contents=sc_excel_table_contents)
    
# 贷款调查——小额贷款
@app.route('/Process/dqdc/show_excel.page/<int:loan_apply_id>/<int:sheet_type>', methods=['GET'])
def show_excel(loan_apply_id,sheet_type):
    sc_excel_table_content = SC_Excel_Table_Content.query.filter_by(loan_apply_id=loan_apply_id,sheet_type=sheet_type).first()
    table_content = base64.b64decode(sc_excel_table_content.table_content).decode("utf-8")
    return render_template("process/dqdc/show_excel.html",table_content=table_content)

# 最后个sheet显示专家建议
@app.route('/Process/dqdc/show_advice.page/<int:application_id>', methods=['GET'])
def show_advice(application_id):
    info = Rcs_Application_Info.query.filter_by(id=application_id).first()
    rcs = Rcs_Application_Advice.query.filter_by(application_id=info.id,user_id=current_user.id).first()

    return render_template("process/dqdc/show_advice.html",loan_apply_id=application_id,rcs=rcs)

# 专家建议保存
@app.route('/Process/dqdc/save_advice/<int:application_id>', methods=['POST'])
def save_advice(application_id):
    try:
        result = request.form['result']
        advice = request.form['advice']
        je = request.form['je']
        info = Rcs_Application_Info.query.filter_by(id=application_id).first()
        rcs = Rcs_Application_Advice.query.filter_by(application_id=info.id,user_id=current_user.id).first()
        if rcs:
            rcs.approve_advice = advice
            rcs.approve_result = result
            rcs.approve_ed = je
            #普通专家
            rcs.advice_type = "1"
        else:
            Rcs_Application_Advice(info.id,advice,result,je,"1").add()
        expert = Rcs_Application_Expert.query.filter_by(application_id=info.id,expert_id=current_user.id).first()
        if expert:
            #设置专家已完成此进件评估
            expert.operate = 1
        #保存进件日志
        Rcs_Application_Log(application_id,info.card_id,info.customer_name,result,je).add()
        db.session.commit()
        flash('保存成功','success')
    except:
        # 回滚
        db.session.rollback()
        logger.exception('exception')
        # 消息闪现
        flash('保存失败','error')
    return redirect("Process/dqdc/show_advice.page/"+str(application_id))