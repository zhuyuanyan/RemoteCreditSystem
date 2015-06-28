#coding:utf-8
from RemoteCreditSystem import db
import datetime

# 进件专家关系表
class Rcs_Application_Expert(db.Model):
    __tablename__ = 'rcs_application_expert'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('rcs_application_info.id'))
    expert_id = db.Column(db.Integer, db.ForeignKey('rcs_user.id'))
    operate = db.Column(db.String(1))

    #外键
    rcs_expert_ibfk_1 = db.relationship('User', backref='rcs_expert_ibfk_1')
    rcs_application_ibfk_2 = db.relationship('Rcs_Application_Info', backref='rcs_application_ibfk_2')

    def __init__(self, application_id,expert_id):
        self.application_id = application_id
        self.expert_id = expert_id
        self.operate = "0"
   
    def add(self):
        db.session.add(self)