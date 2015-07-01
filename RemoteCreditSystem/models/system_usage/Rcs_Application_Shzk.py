#coding:utf-8
from RemoteCreditSystem import db
import datetime
from flask.ext.login import current_user

# 生活状况form
class Rcs_Application_Shzk(db.Model):
    __tablename__ = 'rcs_application_shzk'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer)
    value_1 = db.Column(db.String(5000))
    value_2 = db.Column(db.String(5000))
    value_3 = db.Column(db.String(5000))
    create_user = db.Column(db.String(32))
    create_time = db.Column(db.DateTime)

    def __init__(self, application_id,value_1,value_2,value_3):
        self.application_id = application_id
        self.value_1 = value_1
        self.value_2 = value_2
        self.value_3 = value_3
        self.create_user = current_user.id
        self.create_time = datetime.datetime.now()
   
    def add(self):
        db.session.add(self)