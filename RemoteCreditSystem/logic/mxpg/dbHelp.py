#!/usr/bin/env python
# -*- coding: utf-8 -*-

from RemoteCreditSystem import db
from RemoteCreditSystem.config import logger

class DBHelp():
	def __init__(self,logger):
		# 使用cursor()方法获取操作游标 
		self.cursor = db.cursor()
	
	def executeSql(self,sql,file):
		try:
		   # 执行sql语句
		   sql = sql.replace("\\","")
		   self.cursor.execute(sql)
		   # 提交到数据库执行
		   id = int(self.db.insert_id()) 
		   db.commit()
		   return id
		except Exception,ex: 
		   # Rollback in case there is any error
		   loginfo = "%s-%s-%s" % (file.decode("gbk"),ex,sql)
		   logger.info(loginfo)
		   db.rollback()
		   return -1
		   
	def closeDB(self):
		# 关闭数据库连接
		self.db.close()