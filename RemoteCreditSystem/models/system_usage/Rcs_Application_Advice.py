#coding:utf-8
from RemoteCreditSystem import db
import datetime

# 进件评估结论表
class Rcs_Application_Advice(db.Model):
    __tablename__ = 'rcs_application_advice'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer)
    approve_advice = db.Column(db.String(255))
    approve_result = db.Column(db.String(32))
    approve_ed = db.Column(db.String(32))
    user_id = db.Column(db.String(32))

    def __init__(self, application_id,approve_advice,approve_result,approve_ed,user_id):
        self.application_id = application_id
        self.approve_advice = approve_advice
        self.approve_result = approve_result
        self.approve_ed = approve_ed
        self.user_id = user_id
   
    def add(self):
        db.session.add(self)