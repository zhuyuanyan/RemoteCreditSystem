#coding:utf-8
from RemoteCreditSystem import db
import datetime

# 进件表
class Rcs_Application_Info(db.Model):
    __tablename__ = 'rcs_application_info'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    customer_name = db.Column(db.String(32))
    card_id = db.Column(db.Integer)
    product_name = db.Column(db.String(32))
    approve_je = db.Column(db.String(32))
    approve_org = db.Column(db.String(32))

    def __init__(self, customer_id,customer_name,card_id,product_name,approve_je,approve_org):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.card_id = card_id
        self.product_name = product_name
        self.approve_je = approve_je
        self.approve_org = approve_org

    def add(self):
        db.session.add(self)