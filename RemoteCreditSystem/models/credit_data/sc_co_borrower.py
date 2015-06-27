#coding:utf-8
__author__ = 'Johnny'

from RemoteCreditSystem import db
# 共同借款人
class SC_Co_Borrower(db.Model):
    __tablename__ = 'sc_co_borrower' 
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    name = db.Column(db.String(32)) #姓名
    relationship = db.Column(db.String(32)) #与客户关系
    id_number = db.Column(db.String(32)) #身份证号码
    phone = db.Column(db.String(32)) #家庭电话
    main_business = db.Column(db.String(128))#主营业务或职务（如受雇与别人）
    address = db.Column(db.String(256)) #经营地址或工作单位地址
    major_assets = db.Column(db.String(256)) #主要资产
    monthly_income = db.Column(db.String(16)) #月收入
    home_addr = db.Column(db.String(256)) #家庭详细地址
    hj_addr = db.Column(db.String(256)) #户籍所在地
    home = db.Column(db.String(256)) #住房性质
    remark = db.Column(db.String(256)) #备注

    def __init__(self,loan_apply_id,name,relationship,
                id_number,phone,main_business,address,major_assets,monthly_income,
                home_addr,hj_addr,home,remark):
        self.loan_apply_id = loan_apply_id
        self.name = name
        self.relationship = relationship
        self.id_number = id_number
        self.phone = phone
        self.main_business = main_business
        self.address = address
        self.major_assets = major_assets
        self.monthly_income = monthly_income
        self.home_addr = home_addr
        self.hj_addr = hj_addr
        self.home = home
        self.remark = remark

    def add(self):
        db.session.add(self)