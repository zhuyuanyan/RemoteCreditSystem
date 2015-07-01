#coding:utf-8
from RemoteCreditSystem import db
import datetime

#权限表
class Rcs_Access_Right(db.Model):
    __tablename__ = 'rcs_access_right' 
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer)
    resource_id = db.Column(db.String)
    operations = db.Column(db.Integer)

    def __init__(self,role_id,resource_id, operations):
        self.role_id = role_id
        self.resource_id = resource_id
        self.operations = operations

    def add(self):
        db.session.add(self)