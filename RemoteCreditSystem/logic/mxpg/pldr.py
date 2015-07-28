#coding:utf-8
from flask import Module, session, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user

import datetime
import os
import re
import xdrlib
import xlrd
import json
import base64

from RemoteCreditSystem import db
from RemoteCreditSystem.config import logger
from RemoteCreditSystem.config import LOCALEXCEL_FOLDER_REL
from RemoteCreditSystem.config import LOCALEXCEL_FOLDER_ABS
from RemoteCreditSystem.models.credit_data.sc_local_excel import SC_Local_Excel
from RemoteCreditSystem.models.credit_data.sc_excel_table_content import SC_Excel_Table_Content
import RemoteCreditSystem.tools.parseExcelToHtml as parseExcelToHtml
import RemoteCreditSystem.logic.mxpg.sql as sql
from RemoteCreditSystem.models.system_usage.Rcs_Application_Info import Rcs_Application_Info
from RemoteCreditSystem.models.system_usage.Rcs_Application_Ddpz import Rcs_Application_Ddpz
from RemoteCreditSystem.models.system_usage.Rcs_Application_Shzk import Rcs_Application_Shzk
from RemoteCreditSystem.models.system_usage.Rcs_Application_Jyzk import Rcs_Application_Jyzk

#excel种类
excel_dict = {
                    '建议':{'name':'建议','code':1},
                    '基本状况':{'name':'基本','code':2},
                    '经营状态':{'name':'经营','code':4},
                    '生存状态':{'name':'生存','code':8},
                    '道德品质':{'name':'道德','code':16},
                    '资产负债':{'name':'资产','code':32},
                    '利润简表':{'name':'利润','code':64},
                    '标准利润表':{'name':'标准利润','code':128},
                    '现金流':{'name':'现金','code':256},
                    '交叉检验':{'name':'交叉','code':512},
                    '点货单':{'name':'点货','code':1024},
                    '固定资产':{'name':'固资','code':2048},
                    '应收预付':{'name':'应收预付','code':4096},
                    '应付预收':{'name':'应付预收','code':8192},
                    '流水分析':{'name':'流水','code':16384}
                }

def excel_import(request):
    try:
        customer_name = request.form['customer_name']
        cert_no = request.form['cert_no']
        # 先获取上传文件
        f = request.files['attachment']
        f_old_name = f.filename
        f_suffix_name = f_old_name[f_old_name.rfind('.'):]
        #修改文件名为日期，防止重名
        f_new_name = cert_no+"_"+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+f_suffix_name
        f.filename = f_new_name
        if not os.path.exists(os.path.join(LOCALEXCEL_FOLDER_ABS,str(current_user.id))):
            os.mkdir(os.path.join(LOCALEXCEL_FOLDER_ABS,str(current_user.id)))
        ABS_uri = os.path.join(LOCALEXCEL_FOLDER_ABS,'%d\\%s' % (current_user.id,f.filename))
        REL_uri = os.path.join(LOCALEXCEL_FOLDER_REL,'%d\\%s' % (current_user.id,f.filename))
        
        #上传
        f.save(ABS_uri)
        #存db
        sc_local_excel = SC_Local_Excel(current_user.id,customer_name,cert_no,f_old_name,REL_uri)
        sc_local_excel.add()
        db.session.flush()
        
        #读取excel
        open_excel(sc_local_excel.id,ABS_uri)
        
        # 事务提交
        db.session.commit()
    except:
        # 回滚
        db.session.rollback()
        #抛出异常到view view负责打印
        raise
        
#读取excel
def open_excel(excel_id,ABS_uri):
    id=-1
    data = xlrd.open_workbook(ABS_uri)
    #sheetCount = len(data.sheets())#返回共多少sheet
    for index,sheet in enumerate(data.sheets()):
        #print sheet.name #sheet名称
        if sheet.name.find("建议") != -1:
            id = Genrcs_application_info(sheet)
            table_content = base64.b64encode(parseExcelToHtml.parser(ABS_uri, index))
            SC_Excel_Table_Content(id,excel_id,table_content,excel_dict['建议']['name'],excel_dict['建议']['code']).add()
            break
    
    if id != -1:     
        for d,x in excel_dict.items():
            #print "key:"+d+",value:"+x
            if d != '建议':
                for index,sheet in enumerate(data.sheets()):
                    #print sheet.name #sheet名称
                    if sheet.name == d:
                        table_content = base64.b64encode(parseExcelToHtml.parser(ABS_uri, index))
                        SC_Excel_Table_Content(id,excel_id,table_content,excel_dict[d]['name'],excel_dict[d]['code']).add()
                        break
                
#执行sql
def executeSql(sql):
    sql = sql.replace("\\","")
    db.session.execute(sql)
    return int(db.session.execute("SELECT LAST_INSERT_ID()").fetchone()[0])
    
#进件表
def Genrcs_application_info(sheet):
    customer_name = sheet.row(14)[1].value
    credentials_no = sheet.row(14)[6].value
    
    genSql = sql.sql_rcs_application_info.substitute(customer_name=customer_name,card_id=credentials_no,create_user=current_user.id,create_time=datetime.datetime.now())
    return executeSql(genSql)
    