#coding:utf-8
from RemoteCreditSystem import db
import datetime

# 参数配置表
class Rcs_Parameter(db.Model):
    __tablename__ = 'rcs_parameter'
    id = db.Column(db.Integer, primary_key=True)
    parameter_name = db.Column(db.String(32))
    parameter_value = db.Column(db.String(255))

    def __init__(self, parameter_name,parameter_value):
        self.parameter_name = parameter_name
        self.parameter_value = parameter_value
   
    def add(self):
        db.session.add(self)