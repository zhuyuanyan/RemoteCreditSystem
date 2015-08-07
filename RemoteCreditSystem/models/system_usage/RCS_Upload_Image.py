# coding:utf-8
from RemoteCreditSystem import db
from flask.ext.login import current_user

#影像资料表
class RCS_Upload_Image(db.Model):
	__tablename__ = 'rcs_upload_image'
	id=db.Column(db.Integer, primary_key=True)
	loan_apply_id=db.Column(db.Integer)
	describe=db.Column(db.String(255))
	attachment=db.Column(db.String(255))
	uri=db.Column(db.String(255))
	status=db.Column(db.Integer)#状态 1 正常 2 删除

	def __init__(self,loan_apply_id,describe,attachment,uri):
		self.loan_apply_id = loan_apply_id
		self.describe = describe
		self.attachment = attachment
		self.uri = uri
		self.status = 1

	def add(self):
		db.session.add(self)
