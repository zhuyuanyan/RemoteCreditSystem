#coding:utf-8
from RemoteCreditSystem import db
import datetime
from flask.ext.login import current_user

# 参数配置--下拉框值
class Rcs_Parameter_Select(db.Model):
    __tablename__ = 'rcs_parameter_select'
    id = db.Column(db.Integer, primary_key=True)
    tree_id = db.Column(db.Integer)
    name = db.Column(db.String(255))
    score = db.Column(db.String(32))

    def __init__(self, tree_id,name,score):
        self.tree_id = tree_id
        self.name = name
        self.score = score
   
    def add(self):
        db.session.add(self)