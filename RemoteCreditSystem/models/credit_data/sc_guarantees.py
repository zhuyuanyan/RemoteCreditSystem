#coding:utf-8
__author__ = 'Johnny'

from RemoteCreditSystem import db
# 担保信息
class SC_Guarantees(db.Model):
    __tablename__ = 'sc_guarantees' 
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    name = db.Column(db.String(32)) #姓名
    address = db.Column(db.String(256)) #地址
    id_number = db.Column(db.String(32)) #身份证号码
    workunit = db.Column(db.String(256)) #工作单位
    phone = db.Column(db.String(32)) #电话
    relationship = db.Column(db.String(32)) #与申请人关系
    major_assets = db.Column(db.String(256)) #主要资产
    monthly_income = db.Column(db.String(16)) #月收入
    home_addr = db.Column(db.String(256)) #家庭详细地址
    hj_addr = db.Column(db.String(256)) #户籍所在地
    home = db.Column(db.String(256)) #住房性质
    remark = db.Column(db.String(256)) #备注

    def __init__(self,loan_apply_id,name,address,id_number,
        workunit,phone,relationship,major_assets,monthly_income,home_addr,
        hj_addr,home,remark):
        self.loan_apply_id = loan_apply_id
        self.name = name
        self.address = address
        self.id_number = id_number
        self.workunit = workunit
        self.phone = phone
        self.relationship = relationship
        self.major_assets = major_assets
        self.monthly_income = monthly_income
        self.home_addr = home_addr
        self.hj_addr = hj_addr
        self.home = home
        self.remark = remark

    def add(self):
        db.session.add(self)