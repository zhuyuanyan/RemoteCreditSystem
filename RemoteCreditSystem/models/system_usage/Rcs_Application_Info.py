#coding:utf-8
from RemoteCreditSystem import db
import datetime
from flask.ext.login import current_user

# 进件主表
class Rcs_Application_Info(db.Model):
    __tablename__ = 'rcs_application_info'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer) #客户索引号
    customer_name = db.Column(db.String(32))
    card_id = db.Column(db.Integer)
    product_name = db.Column(db.String(32))
    approve_je = db.Column(db.String(32))
    approve_org = db.Column(db.String(32))
    approve_area = db.Column(db.String(255))
    approve_area_id = db.Column(db.String(32))
    industry = db.Column(db.String(32))
    district = db.Column(db.String(32))
    user_name = db.Column(db.String(32))
    sh_name = db.Column(db.String(32))
    sp_name = db.Column(db.String(32))
    approve_type = db.Column(db.String(1))
    create_user = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)
    model_type = db.Column(db.Integer)

    def __init__(self, customer_id,customer_name,card_id,product_name,approve_je,approve_org,approve_area,approve_area_id,industry,district,user_name,sh_name,sp_name,approve_type,model_type):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.card_id = card_id
        self.product_name = product_name
        self.approve_je = approve_je
        self.approve_org = approve_org
        self.approve_area = approve_area
        self.approve_area_id = approve_area_id
        self.industry = industry
        self.district = district
        self.user_name = user_name
        self.sh_name = sh_name
        self.sp_name = sp_name
        self.approve_type = approve_type
        self.model_type=model_type
        self.create_user=current_user.id
        self.create_time=datetime.datetime.now()
    def add(self):
        db.session.add(self)