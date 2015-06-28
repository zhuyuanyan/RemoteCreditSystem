# coding:utf-8
from RemoteCreditSystem import db
from flask.ext.login import current_user

#客户经理本地数据表
class SC_Local_Excel(db.Model):
	__tablename__ = 'sc_local_excel'
	id=db.Column(db.Integer, primary_key=True)
	user_id=db.Column(db.Integer)
	customer_name=db.Column(db.String(255))
	cert_no=db.Column(db.String(255))
	attachment=db.Column(db.String(255))
	uri=db.Column(db.String(255))

	def __init__(self,user_id,customer_name,cert_no,attachment,uri):
		self.user_id = user_id
		self.customer_name = customer_name
		self.cert_no = cert_no
		self.attachment = attachment
		self.uri = uri

	def add(self):
		db.session.add(self)
