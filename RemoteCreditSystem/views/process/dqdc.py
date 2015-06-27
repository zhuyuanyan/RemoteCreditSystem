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