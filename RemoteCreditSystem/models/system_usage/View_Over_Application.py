#coding:utf-8
from RemoteCreditSystem import db
import datetime
from flask.ext.login import current_user

# 进件超时记录
class View_Over_Application(db.Model):
    __tablename__ = 'view_over_application'
    id = db.Column(db.Integer, primary_key=True)
    expert_id = db.Column(db.Integer)#专家id
    expert_name = db.Column(db.String(32))#专家名称
    over_time = db.Column(db.Date())#超时时间
    app_id = db.Column(db.Integer)#进件id
    app_name = db.Column(db.String(32))#进件名称
    card_id = db.Column(db.String(32))#进件身份id


    def __init__(self, expert_id,expert_name,over_time,app_id,app_name,card_id):
        self.expert_id = expert_id
        self.expert_name = expert_name
        self.over_time = over_time
        self.app_id = app_id
        self.app_name = app_name
        self.card_id = card_id
   
    def add(self):
        db.session.add(self)