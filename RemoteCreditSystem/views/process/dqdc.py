# coding:utf-8
from RemoteCreditSystem import db
from RemoteCreditSystem.config import logger
import RemoteCreditSystem.helpers as helpers
import datetime

from flask import Module, session, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user

from RemoteCreditSystem import app

from RemoteCreditSystem.models import SC_Loan_Apply
from RemoteCreditSystem.models import SC_Apply_Info
from RemoteCreditSystem.models import SC_Loan_Purpose
from RemoteCreditSystem.models import SC_Credit_History
from RemoteCreditSystem.models import SC_Guarantees_For_Others
from RemoteCreditSystem.models import SC_Riskanalysis_And_Findings
from RemoteCreditSystem.models.credit_data.sc_stock import SC_Stock
from RemoteCreditSystem.models.credit_data.sc_individual_customer import SC_Individual_Customer
from RemoteCreditSystem.models.system_usage.Rcs_Application_Advice import Rcs_Application_Advice
from RemoteCreditSystem.models.system_usage.Rcs_Application_Expert import Rcs_Application_Expert



# 贷款调查——小额贷款
@app.route('/Process/dqdc/dqdc_xed/<int:id>', methods=['GET'])
def dqdc_xed(id):
    loan_apply = SC_Loan_Apply.query.filter_by(id=id).first()
    return render_template("Process/dqdc/dqdc_xed.html",loan_apply=loan_apply,id=id)

# 贷款调查——小额贷款(基本情况)
@app.route('/Process/dqdc/dqdcXed_jbqk/<int:id>', methods=['GET'])
def dqdcXed_jbqk(id):
    customer = SC_Individual_Customer.query.filter_by(id="1").first()

    loan_apply = SC_Loan_Apply.query.filter_by(id=id).first()
    apply_info = SC_Apply_Info.query.filter_by(loan_apply_id=id).first()
    loan_purpose = SC_Loan_Purpose.query.order_by("id").all()
    credit_history = SC_Credit_History.query.filter_by(loan_apply_id=id).all()
    guarantees_for_others = SC_Guarantees_For_Others.query.filter_by(loan_apply_id=id).all()
    #financial_overview = SC_Financial_Overview.query.filter_by(loan_apply_id=id).first()
    #non_financial_analysis = SC_Non_Financial_Analysis.query.filter_by(loan_apply_id=id).first()
    riskanalysis_and_findings = SC_Riskanalysis_And_Findings.query.filter_by(loan_apply_id=id).first()
    
    return render_template("Process/dqdc/dqdcXed_jbqk.html",id=id,customer=customer,loan_apply=loan_apply,
        apply_info=apply_info,loan_purpose=loan_purpose,credit_history=credit_history,
        guarantees_for_others=guarantees_for_others,riskanalysis_and_findings=riskanalysis_and_findings)

# 编辑贷款调查——小额贷款(基本情况)
@app.route('/Process/dqdc/edit_dqdcXed_jbqk/<int:id>', methods=['POST'])
def edit_dqdcXed_jbqk(id):
    try:
        riskanalysis_and_findings = SC_Riskanalysis_And_Findings.query.filter_by(loan_apply_id=id).first()
        if riskanalysis_and_findings:
            riskanalysis_and_findings.analysis_conclusion = request.form['analysis_conclusion']
            riskanalysis_and_findings.other_deliberations = request.form['other_deliberations']
            riskanalysis_and_findings.positive = request.form['positive']
            riskanalysis_and_findings.opposite = request.form['opposite']

            verification_list = request.form.getlist('verification')
            riskanalysis_and_findings.verification = 0
            # 循环获取表单
            for i in range(len(verification_list)):
                riskanalysis_and_findings.verification += int(verification_list[i])
            
            riskanalysis_and_findings.others = request.form['others']
            riskanalysis_and_findings.bool_grant = request.form['bool_grant']
            if request.form['bool_grant'] == '1':
                riskanalysis_and_findings.recommended_way_of_security = request.form['recommended_way_of_security']
                riskanalysis_and_findings.income_ratio = request.form['income_ratio']
                riskanalysis_and_findings.amount = request.form['amount']
                riskanalysis_and_findings.deadline = request.form['deadline']
                riskanalysis_and_findings.rates = request.form['rates']
                riskanalysis_and_findings.monthly_repayment = request.form['monthly_repayment']
                riskanalysis_and_findings.approve_reason = request.form['approve_reason']
            else:
                riskanalysis_and_findings.refuse_reason = request.form['refuse_reason']
        else:
            verification_list = request.form.getlist('verification')
            verification_value = 0
            # 循环获取表单
            for i in range(len(verification_list)):
                verification_value += int(verification_list[i])

            SC_Riskanalysis_And_Findings(id,request.form['analysis_conclusion'],
                request.form['recommended_way_of_security'],request.form['income_ratio'],
                verification_value,request.form['others'],
                request.form['bool_grant'],request.form['amount'],
                request.form['deadline'],request.form['rates'],
                request.form['monthly_repayment'],request.form['approve_reason'],
                request.form['refuse_reason'],request.form['other_deliberations'],
                request.form['positive'],request.form['opposite']).add()

        loan_apply = SC_Loan_Apply.query.filter_by(id=id).first()
        # loan_apply.process_status = PROCESS_STATUS_DQDC

        #专家建议保存
        advice = Rcs_Application_Advice.query.filter_by(application_id=id,user_id=current_user.id).first()
        if advice:
            #同意
            if request.form['bool_grant'] == '1':
                advice.approve_advice= request.form['approve_reason']
                advice.approve_result="1"
                advice.approve_ed = request.form['amount']
            else:
                advice.approve_advice= request.form['refuse_reason']
                advice.approve_result="2"
        else:
            #同意
            if request.form['bool_grant'] == '1':
                Rcs_Application_Advice(id,request.form['approve_reason'],"1",request.form['amount']).add()
            else:
                Rcs_Application_Advice(id,request.form['refuse_reason'],"2","").add()
        #专家进件关系表设置为已评估
        expert = Rcs_Application_Expert.query.filter_by(application_id=id,expert_id=current_user.id).first()
        if expert:
            expert.operate="1"
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

    return redirect("Process/dqdc/dqdcXed_jbqk/"+str(id))