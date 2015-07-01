#coding:utf-8
from RemoteCreditSystem import db
import datetime

from flask.ext.login import current_user

# 用户、角色 关联表
class UserRole(db.Model):
    __tablename__ = 'rcs_userrole'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    role_id = db.Column(db.Integer)


    def __init__(self,user_id,role_id):
        self.user_id = user_id
        self.role_id = role_id

    def add(self):
        db.session.add(self)