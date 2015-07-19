#coding:utf-8
from RemoteCreditSystem import db
from flask.ext.login import current_user

# SC_Application_Syb
class SC_Application_Syb(db.Model):
    __tablename__ = 'sc_application_syb'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id = db.Column(db.Integer)
    table_content = db.Column(db.BLOB)
    form_data = db.Column(db.BLOB)

    def __init__(self, loan_apply_id,table_content,form_data):
        self.loan_apply_id = loan_apply_id
        self.table_content = table_content
        self.form_data = form_data
   
    def add(self):
        db.session.add(self)