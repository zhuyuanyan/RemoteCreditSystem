# coding:utf-8
from RemoteCreditSystem import db
from RemoteCreditSystem.config import logger

def deco(func):
	def _deco(*args, **kwargs):
		try:
			func(*args, **kwargs)
			db.session.commit()
			# 消息闪现
			flash('保存成功','success')
		except Exception:
			# 回滚
			db.session.rollback()
			logger.exception('exception')
			# 消息闪现
			flash('保存失败','error')
		return render_template("errors/500.html",error=Exception)
	return _deco