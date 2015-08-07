#coding:utf-8
from RemoteCreditSystem import db
import datetime

# 在线总时长
class Online_Total(db.Model):
    __tablename__ = 'rcs_online_total'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    online_total = db.Column(db.Integer)#在线总时长 分钟

    def __init__(self, user_id,online_total):
        self.user_id = user_id
        self.online_total = online_total

    def add(self):
        db.session.add(self)