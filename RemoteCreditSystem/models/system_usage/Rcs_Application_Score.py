#coding:utf-8
from RemoteCreditSystem import db
import datetime
from flask.ext.login import current_user

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
    create_user = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)
    total_approve = db.Column(db.String(32))
    month_profit = db.Column(db.String(32))

    def __init__(self, application_id,ddpz_score,hknl_score,jyzk_score,shzk_score,remark,total_approve,month_profit):
        self.application_id = application_id
        self.ddpz_score = ddpz_score
        self.hknl_score = hknl_score
        self.jyzk_score = jyzk_score
        self.shzk_score = shzk_score
        self.total_approve = total_approve
        self.shzk_score = shzk_score
        self.create_user= current_user.id
        self.create_time = datetime.datetime.now()
        self.month_profit = month_profit
   
    def add(self):
        db.session.add(self)