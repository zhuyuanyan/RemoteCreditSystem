#coding:utf-8
from RemoteCreditSystem import db
import datetime

# 进件评分表
class Rcs_Application_Score(db.Model):
    __tablename__ = 'rcs_application_score'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer)
    ddpz_score = db.Column(db.String(32))
    hknl_score = db.Column(db.String(32))
    jyzk_score = db.Column(db.String(32))
    shzk_score = db.Column(db.String(32))
    remark = db.Column(db.String(255))

    def __init__(self, application_id,ddpz_score,hknl_score,jyzk_score,shzk_score,remark):
        self.application_id = application_id
        self.ddpz_score = ddpz_score
        self.hknl_score = hknl_score
        self.jyzk_score = jyzk_score
        self.shzk_score = shzk_score
        self.remark = remark
   
    def add(self):
        db.session.add(self)