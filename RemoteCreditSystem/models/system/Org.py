#coding:utf-8
from RemoteCreditSystem import db
import datetime

from flask.ext.login import current_user

# 机构表
class Org(db.Model):
    __tablename__ = 'rcs_org'
    id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(16))
    pId = db.Column(db.Integer)
    open = db.Column(db.Integer)
    levels = db.Column(db.Integer)

    def __init__(self,org_name,pId,levels):
        self.org_name = org_name
        self.pId = pId
        self.open = 1
        self.levels = levels
        
    def add(self):
        db.session.add(self)