#coding:utf-8
from RemoteCreditSystem import db
import datetime
from flask.ext.login import current_user

# 进件缺席记录
class Rcs_Application_Absent(db.Model):
    __tablename__ = 'rcs_application_absent'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer)#进件id
    card_id = db.Column(db.String(32))#身份证
    customer_name = db.Column(db.String(255))#客户名称
    expert_id = db.Column(db.Integer)#专家id
    expert_name = db.Column(db.String(32))#专家名称


    def __init__(self, application_id,card_id,customer_name,expert_id,expert_name):
        self.application_id = application_id
        self.card_id = card_id
        self.customer_name = customer_name
        self.expert_id = expert_id
        self.expert_name = expert_name
   
    def add(self):
        db.session.add(self)