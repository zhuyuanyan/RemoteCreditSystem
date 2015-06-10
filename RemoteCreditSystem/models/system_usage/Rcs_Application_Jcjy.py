#coding:utf-8
from RemoteCreditSystem import db
import datetime

# 交叉检验表
class Rcs_Application_Jcjy(db.Model):
    __tablename__ = 'rcs_application_jcjy'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer)
    value1 = db.Column(db.String(255))
    value2 = db.Column(db.String(255))
    value3 = db.Column(db.String(255))
    value4 = db.Column(db.String(255))
    value5 = db.Column(db.String(255))
    value6 = db.Column(db.String(255))
    value7 = db.Column(db.String(255))
    value8 = db.Column(db.String(255))
    value9 = db.Column(db.String(255))
    value10 = db.Column(db.String(255))
    value11 = db.Column(db.String(255))
    value12 = db.Column(db.String(255))
    value13 = db.Column(db.String(255))
    value14 = db.Column(db.String(255))
    value15 = db.Column(db.String(255))
    value16 = db.Column(db.String(255))
    value17 = db.Column(db.String(255))
    value18 = db.Column(db.String(255))

    def __init__(self, application_id,value1,value2,value3,value4,value5,value6,value7,value8,value9,value10,value11,value12,value13,value14,value15,value16,value17,value18):
        self.application_id = application_id
        self.value1 = value1
        self.value2 = value2
        self.value3 = value3
        self.value4 = value4
        self.value5 = value5
        self.value6 = value6
        self.value7 = value7
        self.value8 = value8
        self.value9 = value9
        self.value10 = value10
        self.value11 = value11
        self.value12 = value12
        self.value13 = value13
        self.value14 = value14
        self.value15 = value15
        self.value16 = value16
        self.value17 = value17
        self.value18 = value18
   
    def add(self):
        db.session.add(self)