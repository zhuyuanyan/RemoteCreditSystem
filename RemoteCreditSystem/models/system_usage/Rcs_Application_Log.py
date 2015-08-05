#coding:utf-8
from RemoteCreditSystem import db
import datetime
from flask.ext.login import current_user

# 进件评估log日志
class Rcs_Application_Log(db.Model):
    __tablename__ = 'rcs_application_log'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer)#进件id
    card_id = db.Column(db.String(32))#身份证
    customer_name = db.Column(db.String(255))#客户名称
    approve_result = db.Column(db.String(32))#进件结果
    approve_ed = db.Column(db.String(32))#授信额度
    expert_id = db.Column(db.String(32))#评估专家id
    expert_name = db.Column(db.String(32))#评估专家名称
    create_time = db.Column(db.DateTime)#评估时间

    def __init__(self, application_id,card_id,customer_name,approve_result,approve_ed):
        self.application_id = application_id
        self.card_id = card_id
        self.customer_name = customer_name
        self.approve_result = approve_result
        self.approve_ed = approve_ed
        self.expert_id = current_user.id
        self.expert_name = current_user.real_name
        self.create_time = datetime.datetime.now()
   
    def add(self):
        db.session.add(self)