#coding:utf-8
from RemoteCreditSystem import db
import datetime

# 角色表
class Role(db.Model):
    __tablename__ = 'rcs_role'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(16))

    def __init__(self, role_name):
        self.role_name = role_name

    def add(self):
        db.session.add(self)