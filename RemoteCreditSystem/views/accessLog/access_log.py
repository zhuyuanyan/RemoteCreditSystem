# coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user

from RemoteCreditSystem import app
from RemoteCreditSystem.config import logger
from RemoteCreditSystem.models import Rcs_Application_Log,Rcs_Application_Absent,View_Over_Application
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
    count = len(Rcs_Application_Log.query.filter(sql).all())
    return render_template("accessLog/accesslog.html",appList=appList,count=count)

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
    count = len(Rcs_Application_Absent.query.filter(sql).all())
    return render_template("accessLog/absentlog.html",appList=appList,count=count)

# 超时专家记录
@app.route('/accessLog/overTime/<int:page>', methods=['POST','GET'])
def overTime(page):
    sql="1=1"
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        card_id = request.form['card_id']
        expert_name = request.form['expert_name']
        if customer_name:
            sql+=" and app_name like '%"+customer_name+"%'"
        if card_id:
            sql+=" and card_id='"+card_id+"'"  
        if expert_name:
            sql+=" and expert_name like '%"+expert_name+"%'"
    sql+=" order by app_id"    
    appList = View_Over_Application.query.filter(sql).paginate(page, per_page = PER_PAGE)
    count = len(View_Over_Application.query.filter(sql).all())
    return render_template("accessLog/overtimelog.html",appList=appList,count=count)
    