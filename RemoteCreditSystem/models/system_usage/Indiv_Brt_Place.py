#coding:utf-8
from RemoteCreditSystem import db
import datetime
from flask.ext.login import current_user

# 区域三级联动
class Indiv_Brt_Place(db.Model):
    __tablename__ = 'indiv_brt_place'
    id = db.Column(db.Integer, primary_key=True)
    type_code = db.Column(db.String(32))
    type_name = db.Column(db.String(32))
    levels = db.Column(db.Integer)
    parent_code = db.Column(db.String(32))


    def __init__(self, type_code,type_name,levels,parent_code):
        self.type_code = type_code
        self.type_name = type_name
        self.levels = levels
        self.parent_code = parent_code
   
    def add(self):
        db.session.add(self)