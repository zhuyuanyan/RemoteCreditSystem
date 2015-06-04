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
    zjzz = db.Column(db.String(32))
    remark1 = db.Column(db.String(255))
    zjqx = db.Column(db.String(32))
    remark2 = db.Column(db.String(255))
    bhxx = db.Column(db.String(32))
    remark3 = db.Column(db.String(255))
    user_type = db.Column(db.String(1))

    def __init__(self,login_name,login_password,real_name,sex,mobile,active,email,card_id,zjzz,remark1,zjqx,remark2,bhxx,remark3,user_type):
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
        self.zjzz = zjzz
        self.remark1 = remark1
        self.zjqx = zjqx
        self.remark2 = remark2
        self.bhxx = bhxx
        self.remark3 = remark3
        self.user_type = user_type
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