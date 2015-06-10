#coding:utf-8
from RemoteCreditSystem import db
import datetime

# 现金流量表
class Rcs_Application_Xjll(db.Model):
    __tablename__ = 'rcs_application_xjll'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer)
    qcxj = db.Column(db.String(255))#期初现金
    jyxxjlr = db.Column(db.String(255))#经营性现金流入
    jyxxjlc = db.Column(db.String(255))#经营性现金流出
    jyxjjll = db.Column(db.String(255))#经营现金净流量
    tzxjlr = db.Column(db.String(255))
    tzxjlc = db.Column(db.String(255))
    tzxjjll = db.Column(db.String(255))
    rzxjlr = db.Column(db.String(255))
    rzxjlc = db.Column(db.String(255))
    rzxjjll = db.Column(db.String(255))
    qmxj = db.Column(db.String(255))
    qcqysd = db.Column(db.String(255))
    qcqyhj = db.Column(db.String(255))
    fxqjsr = db.Column(db.String(255))
    qtsr = db.Column(db.String(255))
    sz = db.Column(db.String(255))
    dxzchj = db.Column(db.String(255))
    zj = db.Column(db.String(255))
    bz = db.Column(db.String(255))
    bwzc = db.Column(db.String(255))

    def __init__(self, application_id,qcxj,jyxxjlr,jyxxjlc,jyxjjll,tzxjlr,tzxjlc,tzxjjll,rzxjlr,rzxjlc,rzxjjll,qmxj,qcqysd,qcqyhj,fxqjsr,qtsr,sz,dxzchj,zj,bz,bwzc):
        self.application_id = application_id
        self.qcxj = qcxj
        self.jyxxjlr = jyxxjlr
        self.jyxxjlc = jyxxjlc
        self.jyxjjll = jyxjjll
        self.tzxjlr = tzxjlr
        self.tzxjlc = tzxjlc
        self.tzxjjll = tzxjjll
        self.rzxjlr = rzxjlr
        self.rzxjlc = rzxjlc
        self.rzxjjll = rzxjjll
        self.qmxj = qmxj
        self.qcqysd = qcqysd
        self.qcqyhj = qcqyhj
        self.fxqjsr = fxqjsr
        self.qtsr = qtsr
        self.sz = sz
        self.dxzchj = dxzchj
        self.zj = zj
        self.bz = bz
        self.bwzc = bwzc

   
    def add(self):
        db.session.add(self)