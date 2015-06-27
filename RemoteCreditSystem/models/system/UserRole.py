#coding:utf-8
from RemoteCreditSystem import db
import datetime

from flask.ext.login import current_user

# 用户、角色 关联表
class UserRole(db.Model):
    __tablename__ = 'rcs_userrole'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('rcs_user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('rcs_role.id'))

    #外键
    rcs_userrole_ibfk_1 = db.relationship('User', backref='rcs_userrole_ibfk_1')
    rcs_userrole_ibfk_2 = db.relationship('Role', backref='rcs_userrole_ibfk_2')

    def __init__(self,user_id,role_id):
        self.user_id = user_id
        self.role_id = role_id

    def add(self):
        db.session.add(self)