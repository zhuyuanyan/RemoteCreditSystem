# coding:utf-8
from RemoteCreditSystem import db
from flask.ext.login import current_user

#客户经理本地数据表
class SC_Excel_Table_Content(db.Model):
	__tablename__ = 'sc_excel_table_content'
	id=db.Column(db.Integer, primary_key=True)
	loan_apply_id=db.Column(db.Integer)
	excel_id=db.Column(db.Integer)
	table_content=db.Column(db.BLOB)
	sheet_name=db.Column(db.String)
	sheet_type=db.Column(db.Integer)

	def __init__(self,loan_apply_id,excel_id,table_content,sheet_name,sheet_type):
		self.loan_apply_id = loan_apply_id
		self.excel_id = excel_id
		self.table_content = table_content
		self.sheet_name = sheet_name
		self.sheet_type = sheet_type

	def add(self):
		db.session.add(self)
