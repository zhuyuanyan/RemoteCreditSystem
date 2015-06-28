#coding:utf-8
from RemoteCreditSystem import db

# 目标客户表
class SC_Target_Customer(db.Model):
    __tablename__ = 'sc_target_customer' 
    id = db.Column(db.Integer, primary_key=True)
    receiver = db.Column(db.Integer) # 接待人
    reception_type = db.Column(db.String(1)) #接待方式 (咨询 0/扫街 1/转介绍 3)

    yingxiao_status = db.Column(db.Integer) # 营销状态
    client_status = db.Column(db.Integer) # 客户状态
    is_apply_form = db.Column(db.Integer) # 是否向小微支行填写申请表？

    customer_name = db.Column(db.String(32)) #客户名称
    mobile = db.Column(db.String(16)) #电话
    sex = db.Column(db.String(1)) #性别
    age = db.Column(db.String(8)) #年龄
    address = db.Column(db.String(128)) #地址
    industry = db.Column(db.Integer) #所属行业
    business_content = db.Column(db.String(256)) #经营内容

    shop_name = db.Column(db.String(128)) #店铺名称
    period = db.Column(db.String(8)) #经营期限
    property_scope = db.Column(db.String(16)) #资产规模(数字)
    monthly_sales = db.Column(db.String(16)) #月销售额
    employees = db.Column(db.String(16)) #雇员数量
    business_type = db.Column(db.Integer) #企业类别

    is_need_loan = db.Column(db.String(256)) #是否有贷款需求

    loan_purpose = db.Column(db.Integer) #贷款目的
    loan_amount = db.Column(db.String(16)) #贷款数额
    repayment_type = db.Column(db.String(64)) #希望的还款方式
    guarantee_type = db.Column(db.String(64)) #能提供的担保方式
    house_property = db.Column(db.String(64)) #房产产权情况
    loan_attention = db.Column(db.String(64)) #贷款关注程度

    is_have_loan = db.Column(db.String(1)) #是否在银行贷过款
    is_known_xhnsh = db.Column(db.String(1)) #知道兴化农商行吗？
    business_with_xhnsh = db.Column(db.String(256)) #您在兴化农村商业银行办理过什么业务？
    is_need_service = db.Column(db.String(1)) #您是否需要办理以下银行产品

    status = db.Column(db.Integer) #状态
    manager = db.Column(db.Integer) #分配主管
    loan_officer = db.Column(db.Integer) #分配客户经理
    loan_officer_date = db.Column(db.DateTime)

    bool_regisiter = db.Column(db.Integer) #已录入
    remark = db.Column(db.String(256)) #备注
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    def __init__(self,receiver,reception_type,yingxiao_status,client_status,is_apply_form,
        customer_name,mobile,sex,age,address,industry,business_content,
        shop_name,period,property_scope,monthly_sales,employees,business_type,is_need_loan,loan_purpose,
        loan_amount,repayment_type,guarantee_type,house_property,loan_attention,is_have_loan,is_known_xhnsh,
        business_with_xhnsh,is_need_service,status,manager,loan_officer,loan_officer_date,bool_regisiter,remark):
        self.receiver = receiver
        self.reception_type = reception_type
        self.yingxiao_status = yingxiao_status
        self.client_status = client_status
        self.is_apply_form = is_apply_form
        self.customer_name = customer_name
        self.mobile = mobile
        self.sex = sex
        self.age = age
        self.address = address
        self.industry = industry
        self.business_content = business_content
        self.shop_name = shop_name
        self.period = period
        self.property_scope = property_scope
        self.monthly_sales = monthly_sales
        self.employees = employees
        self.business_type = business_type
        self.is_need_loan = is_need_loan
        self.loan_purpose = loan_purpose
        self.loan_amount = loan_amount
        self.repayment_type = repayment_type
        self.guarantee_type = guarantee_type
        self.house_property = house_property
        self.loan_attention = loan_attention
        self.is_have_loan = is_have_loan
        self.is_known_xhnsh = is_known_xhnsh
        self.business_with_xhnsh = business_with_xhnsh
        self.is_need_service = is_need_service
        self.status = status
        self.manager = manager
        self.loan_officer = loan_officer
        self.bool_regisiter = bool_regisiter
        self.loan_officer_date = loan_officer_date
        self.remark = remark
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()
        self.modify_user = current_user.id
        self.modify_date = datetime.datetime.now()

    def add(self):
        db.session.add(self)