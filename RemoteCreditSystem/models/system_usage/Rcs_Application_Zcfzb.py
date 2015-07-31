#coding:utf-8
from RemoteCreditSystem import db
import datetime
from flask.ext.login import current_user

# 资产负债表form
class Rcs_Application_Zcfzb(db.Model):
    __tablename__ = 'rcs_application_zcfzb'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer)
    table_value = db.Column(db.String(5000))
    table_content = db.Column(db.BLOB)
    create_user = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)

    def __init__(self, application_id,table_value,table_content):
        self.application_id = application_id
        self.table_value = table_value
        self.table_content = table_content
        self.create_user = current_user.id
        self.create_time = datetime.datetime.now()
   
    def add(self):
        db.session.add(self)