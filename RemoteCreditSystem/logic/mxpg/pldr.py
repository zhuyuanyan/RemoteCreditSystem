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

from RemoteCreditSystem.models.system_usage.Rcs_Application_Lrb import Rcs_Application_Lrb
from RemoteCreditSystem.models.system_usage.Rcs_Application_Xjll import Rcs_Application_Xjll
from RemoteCreditSystem.models.system_usage.Rcs_Application_Zcfzb import Rcs_Application_Zcfzb
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

#需要读取数据的几张表
letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

#资产负债表
zcfcb_arr = [
             "5-G","5-I","5-P","5-R",
             "6-G","6-I","6-P","6-R",
             "7-G","7-I","7-P","7-R",
             "8-G","8-I","8-P","8-R",
             "9-G","9-I","9-P","9-R",
             "10-G","10-I","10-P","10-R",
             "11-G","11-I","11-P","11-R",
             "12-G","12-I","12-P","12-R",
             "13-G","13-I","13-P","13-R",
             "14-G","14-I","14-P","14-R",
             "15-G","15-I","15-P","15-R",
             "16-G","16-I","16-P","16-R",
             "17-G","17-I","17-P","17-R",
             "18-E","18-I","18-P",
             "20-R",
             "24-A","24-D","24-F","24-H","24-I","24-L","24-N","24-P","24-Q","24-R",
             "25-A","25-D","25-F","25-H","25-I","25-L","25-N","25-P","25-Q","25-R",
             "26-A","26-D","26-F","26-H","26-I","26-L","26-N","26-P","26-Q","26-R",
             "27-A","27-D","27-F","27-H","27-I","27-L","27-N","27-P","27-Q","27-R",
             "28-A","28-D","28-F","28-H","28-I","28-L","28-N","28-P","28-Q","28-R",
             "29-A","29-D","29-F","29-H","29-I","29-L","29-N","29-P","29-Q","29-R",
             "30-A","30-D","30-F","30-H","30-I","30-L","30-N","30-P","30-Q","30-R",
             "32-R",
             "36-I","36-R",
             "37-I","37-R"
             ]
#利润简表
lrb_arr = [
           "4-C","4-D","4-E","4-F",
           "5-C","5-D","5-E","5-F",
           "6-C","6-D","6-E","6-F","6-G","6-H",
           "7-C","7-D","7-E","7-F","7-G","7-H",
           "8-C","8-D","8-E","8-F","8-G","8-H",
           "9-B","9-C","9-D","9-E","9-F","9-G","9-H",
           "10-B","10-C","10-D","10-E","10-F","10-G","10-H",
           "11-B","11-C","11-D","11-E","11-F","11-G","11-H",
           "12-B","12-C","12-D","12-E","12-F","12-G","12-H",
           "13-B","13-C","13-D","13-E","13-F","13-G","13-H",
           "14-B","14-C","14-D","14-E","14-F","14-G","14-H",
           "15-B","15-C","15-D","15-E","15-F","15-G","15-H",
           "16-B","16-C","16-D","16-E","16-F","16-G","16-H",
           "17-B","17-C","17-D","17-E","17-F","17-G","17-H",
           "18-B","18-C","18-D","18-E","18-F","18-G","18-H",
           "19-B","19-C","19-D","19-E","19-F","19-G","19-H",
           "20-B","20-C","20-D","20-E","20-F","20-G","20-H",
           "21-B","21-C","21-D","21-E","21-F","21-G","21-H",
           "22-B","22-C","22-D","22-E","22-F","22-G","22-H",
           "23-B","23-C","23-D","23-E","23-F","23-G","23-H",
           "24-C","24-D","24-E","24-F","24-G","24-H",
           "25-C","25-D","25-E","25-F","25-G","25-H",
           "26-C","26-D","26-E","26-F","26-G","26-H",
           "27-C","27-D","27-E","27-F","27-G","27-H",
           "28-C","28-D","28-E","28-F","28-G","28-H",
           "29-C","29-D","29-E","29-F","29-G","29-H",
           "30-C","30-D","30-E","30-F","30-G","30-H",
           "31-C","31-D","31-E","31-F","31-G","31-H",
           "32-H",
           "33-D","33-H",
           "34-B","34-E","34-H"
           ]
#现金流
xjl_arr = [
           "4-C","4-D","4-E","4-F","4-G","4-H","4-I","4-J","4-K","4-L","4-M","4-N","4-O","4-P",
           "5-C","5-D","5-E","5-F","5-G","5-H","5-I","5-J","5-K","5-L","5-M","5-N","5-O","5-P",
           "6-C","6-D","6-E","6-F","6-G","6-H","6-I","6-J","6-K","6-L","6-M","6-N","6-O","6-P",
           "7-C","7-D","7-E","7-F","7-G","7-H","7-I","7-J","7-K","7-L","7-M","7-N","7-O","7-P",
           "8-C","8-D","8-E","8-F","8-G","8-H","8-I","8-J","8-K","8-L","8-M","8-N","8-O","8-P",
           "9-C","9-D","9-E","9-F","9-G","9-H","9-I","9-J","9-K","9-L","9-M","9-N","9-O","9-P",
           "10-C","10-D","10-E","10-F","10-G","10-H","10-I","10-J","10-K","10-L","10-M","10-N","10-O","10-P",
           "11-C","11-D","11-E","11-F","11-G","11-H","11-I","11-J","11-K","11-L","11-M","11-N","11-O","11-P",
           "12-C","12-D","12-E","12-F","12-G","12-H","12-I","12-J","12-K","12-L","12-M","12-N","12-O","12-P",
           "13-C","13-D","13-E","13-F","13-G","13-H","13-I","13-J","13-K","13-L","13-M","13-N","13-O","13-P",
           "14-C","14-D","14-E","14-F","14-G","14-H","14-I","14-J","14-K","14-L","14-M","14-N","14-O","14-P",
           "15-C","15-D","15-E","15-F","15-G","15-H","15-I","15-J","15-K","15-L","15-M","15-N","15-O","15-P",
           "16-C","16-D","16-E","16-F","16-G","16-H","16-I","16-J","16-K","16-L","16-M","16-N","16-O","16-P",
           "17-C","17-D","17-E","17-F","17-G","17-H","17-I","17-J","17-K","17-L","17-M","17-N","17-O","17-P",
           "18-C","18-D","18-E","18-F","18-G","18-H","18-I","18-J","18-K","18-L","18-M","18-N","18-O","18-P",
           "19-C","19-D","19-E","19-F","19-G","19-H","19-I","19-J","19-K","19-L","19-M","19-N","19-O","19-P",
           "20-C","20-D","20-E","20-F","20-G","20-H","20-I","20-J","20-K","20-L","20-M","20-N","20-O","20-P",
           "21-C","21-D","21-E","21-F","21-G","21-H","21-I","21-J","21-K","21-L","21-M","21-N","21-O","21-P",
           "22-C","22-D","22-E","22-F","22-G","22-H","22-I","22-J","22-K","22-L","22-M","22-N","22-O","22-P",
           "23-C","23-D","23-E","23-F","23-G","23-H","23-I","23-J","23-K","23-L","23-M","23-N","23-O","23-P",
           "24-C","24-D","24-E","24-F","24-G","24-H","24-I","24-J","24-K","24-L","24-M","24-N","24-O","24-P",
           "25-C","25-D","25-E","25-F","25-G","25-H","25-I","25-J","25-K","25-L","25-M","25-N","25-O","25-P",
           "26-C","26-D","26-E","26-F","26-G","26-H","26-I","26-J","26-K","26-L","26-M","26-N","26-O","26-P",
           "27-C","27-D","27-E","27-F","27-G","27-H","27-I","27-J","27-K","27-L","27-M","27-N","27-O","27-P",
           "28-C","28-D","28-E","28-F","28-G","28-H","28-I","28-J","28-K","28-L","28-M","28-N","28-O","28-P",
           "29-C","29-D","29-E","29-F","29-G","29-H","29-I","29-J","29-K","29-L","29-M","29-N","29-O","29-P",
           "30-C","30-D","30-E","30-F","30-G","30-H","30-I","30-J","30-K","30-L","30-M","30-N","30-O","30-P",
           "31-C","31-D","31-E","31-F","31-G","31-H","31-I","31-J","31-K","31-L","31-M","31-N","31-O","31-P",
           "32-C","32-D","32-E","32-F","32-G","32-H","32-I","32-J","32-K","32-L","32-M","32-N","32-O","32-P",
           "33-C","33-D","33-E","33-F","33-G","33-H","33-I","33-J","33-K","33-L","33-M","33-N","33-O","33-P",
           "34-C","34-D","34-E","34-F","34-G","34-H","34-I","34-J","34-K","34-L","34-M","34-N","34-O","34-P",
           "35-H","35-P"
           ]

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
                        
                        #读数据
                        tmp = ''
                        if sheet.name == '资产负债':
                            for i in range(0, len(zcfcb_arr)):
                                arr = zcfcb_arr[i].split['-']
                                tmp += sheet.row_values(int(arr[0]))[letters.index(arr[1])] + "@@"
                            tmp = tmp[0:len(tmp)-2]
                            Rcs_Application_Zcfzb(id,tmp).add()
                        if sheet.name == '利润简表':
                            for i in range(0, len(lrb_arr)):
                                arr = lrb_arr[i].split['-']
                                tmp += sheet.row_values(int(arr[0]))[letters.index(arr[1])] + "@@"
                            tmp = tmp[0:len(tmp)-2]
                            Rcs_Application_Lrb(id,tmp).add()
                        if sheet.name == '现金流':
                            for i in range(0, len(xjl_arr)):
                                arr = xjl_arr[i].split['-']
                                tmp += sheet.row_values(int(arr[0]))[letters.index(arr[1])] + "@@"
                            tmp = tmp[0:len(tmp)-2]
                            Rcs_Application_Xjll(id,tmp).add()
                            
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
    