#coding:utf-8
from RemoteCreditSystem import db
import datetime

# 在线历时
class Online_Current(db.Model):
    __tablename__ = 'rcs_online_current'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    online_current = db.Column(db.Integer)#本次在线时长 分钟

    def __init__(self, user_id,online_current):
        self.user_id = user_id
        self.online_current = online_current

    def add(self):
        db.session.add(self)