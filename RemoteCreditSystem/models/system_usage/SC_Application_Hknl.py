#coding:utf-8
from RemoteCreditSystem import db
from flask.ext.login import current_user

# SC_Application_Hknl
class SC_Application_Hknl(db.Model):
    __tablename__ = 'sc_application_hknl'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id = db.Column(db.Integer)
    form_data = db.Column(db.BLOB)

    def __init__(self, loan_apply_id,form_data):
        self.loan_apply_id = loan_apply_id
        self.form_data = form_data
   
    def add(self):
        db.session.add(self)