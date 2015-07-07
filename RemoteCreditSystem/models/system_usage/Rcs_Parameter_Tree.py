#coding:utf-8
from RemoteCreditSystem import db
import datetime
from flask.ext.login import current_user

# 参数配置--左边树节点
class Rcs_Parameter_Tree(db.Model):
    __tablename__ = 'rcs_parameter_tree'
    id = db.Column(db.Integer, primary_key=True)
    param_type = db.Column(db.String(32))
    name = db.Column(db.String(255))
    pId = db.Column(db.Integer)
    weight = db.Column(db.String(32))
    level_type = db.Column(db.Integer)
    create_user = db.Column(db.Integer)

    def __init__(self, param_type,name,pId,weight,level_type):
        self.param_type = param_type
        self.name = name
        self.pId = pId
        self.weight = weight
        self.level_type = level_type
        self.create_user = current_user.id
   
    def add(self):
        db.session.add(self)