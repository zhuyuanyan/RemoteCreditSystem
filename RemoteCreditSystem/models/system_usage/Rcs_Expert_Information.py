#coding:utf-8
from RemoteCreditSystem import db
import datetime
from flask.ext.login import current_user

# 专家信息
class Rcs_Expert_Information(db.Model):
    __tablename__ = 'rcs_expert_information'
    id = db.Column(db.Integer, primary_key=True)
    expert_id = db.Column(db.Integer)#专家id
    address = db.Column(db.String(255))#常驻地址
    hy = db.Column(db.String(255))#行业
    qy = db.Column(db.String(255))#区域
    product = db.Column(db.String(32))#产品
    balance = db.Column(db.String(32))#授信余额
    zyzc = db.Column(db.String(32))#专业职称
    xrzw = db.Column(db.String(32))#现任职务
    expert_level = db.Column(db.String(32))#专家层级
    approve_role = db.Column(db.String(32))#授信评估权限
    gzr = db.Column(db.String(32))#工作日
    gzsd = db.Column(db.String(32))#工作时段


    def __init__(self,expert_id,address,hy,qy,product,balance,zyzc,xrzw,expert_level,approve_role,gzr,gzsd):
        self.expert_id = expert_id
        self.address = address
        self.hy = hy
        self.qy = qy
        self.product = product
        self.balance = balance
        self.zyzc = zyzc
        self.xrzw = xrzw
        self.expert_level = expert_level
        self.approve_role = approve_role
        self.gzr = gzr
        self.gzsd = gzsd
   
    def add(self):
        db.session.add(self)