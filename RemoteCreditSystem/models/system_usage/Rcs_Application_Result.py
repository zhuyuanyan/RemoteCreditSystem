#coding:utf-8
from RemoteCreditSystem import db
import datetime

# 还款能力结果表
class Rcs_Application_Result(db.Model):
    __tablename__ = 'rcs_application_result'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer)
    zcfzl = db.Column(db.String(255))#资产负债率
    ldbl = db.Column(db.String(255))#流动比率
    sdbl = db.Column(db.String(255))#速动比率
    value_1 = db.Column(db.String(255))#存货总额
    value_2 = db.Column(db.String(255))#总资产
    value_3 = db.Column(db.String(255))#流动资产总和
    chzzl = db.Column(db.String(255))#存货周转率
    zzczzl = db.Column(db.String(255))#总资产周转率
    value_13 = db.Column(db.String(255))#净利润

    def __init__(self, application_id,zcfzl,ldbl,sdbl,value_1,value_2,value_3,chzzl,zzczzl,value_13):
        self.application_id = application_id
        self.zcfzl = zcfzl
        self.ldbl = ldbl
        self.sdbl = sdbl
        self.value_1 = value_1
        self.value_2 = value_2
        self.value_3 = value_3
        self.chzzl = chzzl
        self.zzczzl = zzczzl
        self.value_13 = value_13
    def add(self):
        db.session.add(self)