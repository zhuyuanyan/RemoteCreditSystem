#coding:utf-8
from RemoteCreditSystem import db
import datetime
from flask.ext.login import current_user

# 拒绝评估任务记录
class Rcs_Expert_Refuse(db.Model):
    __tablename__ = 'rcs_expert_refuse'
    id = db.Column(db.Integer, primary_key=True)
    expert_id = db.Column(db.Integer)#专家id
    expert_name = db.Column(db.String(32))#专家名称
    application_id = db.Column(db.Integer)#进件id
    application_name = db.Column(db.String(255))#进件名称
    reason = db.Column(db.String(255))#专家名称
    new_expert_id = db.Column(db.Integer)#重选专家id
    new_expert_name = db.Column(db.String(32))#重选专家名称
    create_time = db.Column(db.DateTime)#创建时间


    def __init__(self, expert_id,expert_name,application_id,application_name,reason,new_expert_id,new_expert_name):
        self.application_id = application_id
        self.application_name = application_name
        self.expert_id = expert_id
        self.expert_name = expert_name
        self.reason = reason
        self.new_expert_id = new_expert_id
        self.new_expert_name = new_expert_name
        self.create_time = datetime.datetime.now()
   
    def add(self):
        db.session.add(self)