#coding:utf-8
from RemoteCreditSystem import db
import datetime

from flask.ext.login import current_user

# 用户表
class User(db.Model):
    __tablename__ = 'rcs_user'
    id = db.Column(db.Integer, primary_key=True)
    login_name = db.Column(db.String(16))
    login_password = db.Column(db.String(32))
    real_name = db.Column(db.String(32))
    sex = db.Column(db.String(1))
    mobile = db.Column(db.String(16))
    active = db.Column(db.String(1))
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)
    email = db.Column(db.String(100))
    card_id = db.Column(db.String(32))
    user_type = db.Column(db.String(1))
    org_id = db.Column(db.Integer)
    pId = db.Column(db.Integer)

    def __init__(self,login_name,login_password,real_name,sex,mobile,active,email,card_id,user_type,
                 org_id,pId):
        self.login_name = login_name
        self.login_password = login_password
        self.real_name = real_name
        self.sex = sex
        self.mobile = mobile
        self.active = active
        self.create_date = datetime.datetime.now()
        self.modify_date = datetime.datetime.now()
        self.email = email
        self.card_id = card_id
        self.user_type = user_type        
        self.org_id = org_id
        self.pId = pId
        
    def add(self):
        db.session.add(self)

    # flask-login 需要的4个函数---start
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    # flask-login 需要的4个函数---end