#coding:utf-8
__author__ = 'Johnny'

from RemoteCreditSystem import db
# 有无抵押物
class SC_Guaranty(db.Model):
    __tablename__ = 'sc_guaranty' 
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    obj_name = db.Column(db.String(32)) #物品名称
    owner_address = db.Column(db.String(128)) #所有者、地址
    description = db.Column(db.String(256)) #描述
    registration_number = db.Column(db.String(32)) #登记号
    appraisal = db.Column(db.String(16)) #估价(元)
    mortgage = db.Column(db.String(16)) #抵押(元)
    bool_mortgage = db.Column(db.Integer) #是否抵押

    def __init__(self,loan_apply_id,obj_name,owner_address,description,
        registration_number,appraisal,mortgage,bool_mortgage):
        self.loan_apply_id = loan_apply_id
        self.obj_name = obj_name
        self.owner_address = owner_address
        self.description = description
        self.registration_number = registration_number
        self.appraisal = appraisal
        self.mortgage = mortgage
        self.bool_mortgage = bool_mortgage

    def add(self):
        db.session.add(self)