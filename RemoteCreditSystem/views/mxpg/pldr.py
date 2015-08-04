# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user

from RemoteCreditSystem import app
from RemoteCreditSystem.config import logger
import RemoteCreditSystem.logic.mxpg.pldr as pldr
 
# 导入excel
@app.route('/pldr/excel_import', methods=['POST','GET'])
def excel_import():
    if request.method == 'POST':
        try:
            pldr.excel_import(request)
            # 消息闪现
            flash('保存成功','success')
        except:
            logger.exception('exception')
            # 消息闪现
            flash('保存失败','error')
        return redirect("/mxpg/pldr/1")
    else:
        return redirect("/mxpg/pldr/1")
