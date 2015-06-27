#coding:utf-8
from RemoteCreditSystem import db
import datetime

#权限表
class Rcs_Privilege(db.Model):
    __tablename__ = 'rcs_privilege' 
    id = db.Column(db.Integer, primary_key=True)
    privilege_master = db.Column(db.String(32))
    privilege_master_id = db.Column(db.Integer)
    privilege_access = db.Column(db.String(32))
    privilege_access_value = db.Column(db.String(32))
    privilege_operation = db.Column(db.String)

    def __init__(self,privilege_master,privilege_master_id, privilege_access,privilege_access_value,privilege_operation):
        self.privilege_master = privilege_master
        self.privilege_master_id = privilege_master_id
        self.privilege_access = privilege_access
        self.privilege_access_value = privilege_access_value
        self.privilege_operation = privilege_operation

    def add(self):
        db.session.add(self)