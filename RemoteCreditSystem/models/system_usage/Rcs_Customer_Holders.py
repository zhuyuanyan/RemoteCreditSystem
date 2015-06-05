#coding:utf-8
from RemoteCreditSystem import db
import datetime

# 客户股东表
class Rcs_Customer_Information(db.Model):
    __tablename__ = 'rcs_customer_holders'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(255))
    customer_type = db.Column(db.String(255))
    area = db.Column(db.String(255))
    yyzz_id = db.Column(db.String(255))
    zzjg_id = db.Column(db.String(255))
    zczb_capital = db.Column(db.String(255))
    sszb_capital = db.Column(db.String(255))
    create_time = db.Column(db.String(255))
    zcdz_address = db.Column(db.String(255))
    bgdz_address = db.Column(db.String(255))
    gswz_online = db.Column(db.String(255))
    frdb_name = db.Column(db.String(255))
    frdb_position = db.Column(db.String(255))
    frdb_phone = db.Column(db.String(255))
    frdb_email = db.Column(db.String(255))
    enterprise_name = db.Column(db.String(255))
    enterprise_position = db.Column(db.String(255))
    enterprise_phone = db.Column(db.String(255))
    enterprise_email = db.Column(db.String(255))

    def __init__(self,customer_name,customer_type,area,yyzz_id,zzjg_id,zczb_capital,sszb_capital,create_time,zcdz_address,bgdz_address,gswz_online,frdb_name,frdb_position,frdb_phone,frdb_email,enterprise_name,enterprise_position,enterprise_phone,enterprise_email):
        self.customer_name = customer_name
        self.customer_type = customer_type
        self.area = area
        self.yyzz_id = yyzz_id
        self.zzjg_id = zzjg_id
        self.zczb_capital = zczb_capital
        self.sszb_capital = sszb_capital
        self.create_time = create_time
        self.zcdz_address = zcdz_address
        self.bgdz_address = bgdz_address
        self.gswz_online = gswz_online
        self.frdb_name = frdb_name
        self.frdb_position = frdb_position
        self.frdb_phone = frdb_phone
        self.frdb_email = frdb_email
        self.enterprise_name = enterprise_name
        self.enterprise_position = enterprise_position
        self.enterprise_phone = enterprise_phone
        self.enterprise_email = enterprise_email
    def add(self):
        db.session.add(self)