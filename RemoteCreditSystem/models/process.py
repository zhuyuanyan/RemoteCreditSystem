#coding:utf-8
from flask.ext.login import current_user

from RemoteCreditSystem import db
import datetime

# 贷款申请
class SC_Loan_Apply(db.Model):
    __tablename__ = 'sc_loan_apply' 
    id = db.Column(db.Integer, primary_key=True)
    loan_type = db.Column(db.Integer) #贷款类型
    belong_customer_type = db.Column(db.String(32)) #客户类型 Company 或者 Individual
    belong_customer_value = db.Column(db.Integer) #客户id
    customer_name = db.Column(db.String(128)) #处理状态
    evaluation = db.Column(db.String(256)) #评价
    marketing_loan_officer = db.Column(db.Integer) #营销信贷员
    A_loan_officer = db.Column(db.Integer) #A岗信贷员
    B_loan_officer = db.Column(db.Integer) #B岗信贷员
    yunying_loan_officer = db.Column(db.Integer) #运营岗信贷员
    examiner_1 = db.Column(db.Integer) #审查人
    examiner_2 = db.Column(db.Integer) #审查人
    approver = db.Column(db.Integer) #审批人
    process_status = db.Column(db.String(4)) #处理状态
    classify = db.Column(db.Integer) #资产分类
    classify_dec = db.Column(db.String(256)) #资产分类说明
    risk_level = db.Column(db.Integer) #营销信贷员
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)
   


    def __init__(self,loan_type,belong_customer_type,belong_customer_value,customer_name,
        evaluation,marketing_loan_officer,A_loan_officer,B_loan_officer,
        yunying_loan_officer,examiner_1,examiner_2,approver,process_status,risk_level):
        self.loan_type = loan_type
        self.belong_customer_type = belong_customer_type
        self.belong_customer_value = belong_customer_value
        self.customer_name = customer_name
        self.evaluation = evaluation
        self.marketing_loan_officer = marketing_loan_officer
        self.A_loan_officer = A_loan_officer
        self.B_loan_officer = B_loan_officer
        self.yunying_loan_officer = yunying_loan_officer
        self.examiner_1 = examiner_1
        self.examiner_2 = examiner_2
        self.approver = approver
        self.process_status = process_status
        self.classify = 1
        self.classify_dec = ''
        self.risk_level = risk_level
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)

# 申请信息
class SC_Apply_Info(db.Model):
    __tablename__ = 'sc_apply_info' 
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    loan_amount_num = db.Column(db.String(16)) #贷款金额（元）
    loan_deadline = db.Column(db.String(16)) #贷款期限（月）
    month_repayment = db.Column(db.String(16)) #月还款能力（元）
    loan_purpose = db.Column(db.Integer) #贷款用途
    details = db.Column(db.String(256))#详细说明
    repayment_source = db.Column(db.String(256)) #还款来源
    #repayment_type = db.Column(db.Integer) #还款方式
    #annual_interest_rate = db.Column(db.String(16)) #月利率
    

    def __init__(self,loan_apply_id,loan_amount_num,loan_deadline,
                month_repayment,loan_purpose,details,repayment_source):
        self.loan_apply_id = loan_apply_id
        self.loan_amount_num = loan_amount_num
        self.loan_deadline = loan_deadline
        self.month_repayment = month_repayment
        self.loan_purpose = loan_purpose
        self.details = details
        self.repayment_source = repayment_source

    def add(self):
        db.session.add(self)

# 贷款用途 loan
class SC_Loan_Purpose(db.Model):
    __tablename__ = 'sc_loan_purpose'
    id=db.Column(db.Integer, primary_key=True)
    type_name=db.Column(db.String(16))

    def __init__(self, type_name):
        self.type_name = type_name
        
    def add(self):
        db.session.add(self)

# 信贷历史
class SC_Credit_History(db.Model):
    __tablename__ = 'sc_credit_history' 
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    financing_sources = db.Column(db.String(256)) #融资来源
    loan_amount = db.Column(db.String(16)) #贷款金额(元)
    deadline = db.Column(db.String(16)) #期限
    use = db.Column(db.String(256)) #用途
    release_date = db.Column(db.Date)#发放日期
    overage = db.Column(db.String(16)) #余额(元)
    guarantee = db.Column(db.String(32)) #担保
    late_information = db.Column(db.String(256)) #逾期信息

    def __init__(self,loan_apply_id,financing_sources,loan_amount,
                deadline,use,release_date,overage,guarantee,late_information):
        self.loan_apply_id = loan_apply_id
        self.financing_sources = financing_sources
        self.loan_amount = loan_amount
        self.deadline = deadline
        self.use = use
        self.release_date = release_date
        self.overage = overage
        self.guarantee = guarantee
        self.late_information = late_information

    def add(self):
        db.session.add(self)

# 是否为他人担保
class SC_Guarantees_For_Others(db.Model):
    __tablename__ = 'sc_guarantees_for_others' 
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    bank = db.Column(db.String(32)) #银行
    guarantor = db.Column(db.String(32)) #被担保人
    guarantee_amount = db.Column(db.String(16)) #担保金额

    def __init__(self,loan_apply_id,bank,guarantor,guarantee_amount):
        self.loan_apply_id = loan_apply_id
        self.bank = bank
        self.guarantor = guarantor
        self.guarantee_amount = guarantee_amount

    def add(self):
        db.session.add(self)

# 风险分析以及调查结论
class SC_Riskanalysis_And_Findings(db.Model):
    __tablename__ = 'sc_riskanalysis_and_findings' 
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    analysis_conclusion = db.Column(db.String(256)) #分析结论
    recommended_way_of_security = db.Column(db.String(32)) #建议担保方式
    income_ratio = db.Column(db.String(32)) #月付款占可支配收入比重
    verification = db.Column(db.Integer) #客户信息收集与核实
    others = db.Column(db.String(256)) #其他
    bool_grant = db.Column(db.String(1)) #是否发放(建议)
    amount = db.Column(db.String(32)) #金额(元)
    deadline = db.Column(db.String(32)) #期限
    rates = db.Column(db.String(32)) #利率
    monthly_repayment = db.Column(db.String(32)) #月还款额（元）
    approve_reason = db.Column(db.String(256)) #建议理由/发放条件
    refuse_reason = db.Column(db.String(256)) #否决原因

    other_deliberations=db.Column(db.String(256))#其他审议内容
    positive=db.Column(db.String(256))#正
    opposite=db.Column(db.String(256))#反

    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    def __init__(self,loan_apply_id,analysis_conclusion,recommended_way_of_security,income_ratio,
        verification,others,bool_grant,amount,deadline,rates,
        monthly_repayment,approve_reason,refuse_reason,
        other_deliberations,positive,opposite):
        self.loan_apply_id = loan_apply_id
        self.analysis_conclusion = analysis_conclusion
        self.recommended_way_of_security = recommended_way_of_security
        self.income_ratio = income_ratio
        self.verification = verification
        self.others = others
        self.bool_grant = bool_grant
        self.amount = amount
        self.deadline = deadline
        self.rates = rates
        self.monthly_repayment = monthly_repayment
        self.approve_reason = approve_reason
        self.refuse_reason = refuse_reason
        self.other_deliberations = other_deliberations
        self.positive = positive
        self.opposite = opposite
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)



