#coding:utf-8
from RemoteCreditSystem import db
from flask.ext.login import current_user

# SC_Application_Xjllb
class SC_Application_Xjllb(db.Model):
    __tablename__ = 'sc_application_xjllb'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id = db.Column(db.Integer)
    table_content = db.Column(db.BLOB)

    def __init__(self, loan_apply_id,table_content):
        self.loan_apply_id = loan_apply_id
        self.table_content = table_content
   
    def add(self):
        db.session.add(self)