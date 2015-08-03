# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user

from RemoteCreditSystem import app
from RemoteCreditSystem.config import logger
from RemoteCreditSystem.models import Rcs_Application_Log,Rcs_Application_Absent
from RemoteCreditSystem.config import PER_PAGE
 
# 评估日志
@app.route('/accessLog/list/<int:page>', methods=['POST','GET'])
def list(page):
    sql="1=1"
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        card_id = request.form['card_id']
        if customer_name:
            sql+=" and customer_name like '%"+customer_name+"%'"
        if card_id:
            sql+=" and card_id='"+card_id+"'"  
    sql+=" order by application_id"    
    appList = Rcs_Application_Log.query.filter(sql).paginate(page, per_page = PER_PAGE)
    return render_template("accessLog/accesslog.html",appList=appList)

# 缺席专家记录
@app.route('/accessLog/absent/<int:page>', methods=['POST','GET'])
def absent(page):
    sql="1=1"
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        card_id = request.form['card_id']
        expert_name = request.form['expert_name']
        if customer_name:
            sql+=" and customer_name like '%"+customer_name+"%'"
        if card_id:
            sql+=" and card_id='"+card_id+"'"  
        if expert_name:
            sql+=" and expert_name like '%"+expert_name+"%'"
    sql+=" order by application_id"    
    appList = Rcs_Application_Absent.query.filter(sql).paginate(page, per_page = PER_PAGE)
    return render_template("accessLog/absentlog.html",appList=appList)
    