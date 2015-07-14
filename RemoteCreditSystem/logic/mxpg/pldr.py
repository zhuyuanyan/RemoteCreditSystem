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
                    '基本':{'name':'基本情况','code':"1"},
                    '资负':{'name':'资产负债表','code':"2"},
                    '经营':{'name':'经营信息','code':"4"},
                    '损益':{'name':'损益表','code':"8"},
                    '交叉':{'name':'交叉检验','code':"16"},
                    '点货':{'name':'点货单','code':"32"},
                    '固资':{'name':'固定资产','code':"64"}
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
    data = xlrd.open_workbook(ABS_uri)
    #sheetCount = len(data.sheets())#返回共多少sheet
    for index,sheet in enumerate(data.sheets()):
        #print sheet.name #sheet名称
        if sheet.name.find("基本") != -1:
            customer_no = GenTargetCustomer(sheet)
            customer_id = GenIndividualCustomer(sheet,customer_no)
            id = GenLoanApply(sheet,customer_id)
            Genrcs_application_info(sheet,customer_id,id)
            GenApplyInfo(sheet,id)
            GenOthers(sheet,id)
            table_content = base64.b64encode(parseExcelToHtml.parser(ABS_uri, index))
            SC_Excel_Table_Content(id,excel_id,table_content,excel_dict['基本']['name'],excel_dict['基本']['code']).add()
        if sheet.name.find("资负") != -1:
            GenZCFZB(sheet,id)
            table_content = base64.b64encode(parseExcelToHtml.parser(ABS_uri, index))
            SC_Excel_Table_Content(id,excel_id,table_content,excel_dict['资负']['name'],excel_dict['资负']['code']).add()
        if sheet.name.find("经营") != -1:
            GenJY(sheet,id)
            table_content = base64.b64encode(parseExcelToHtml.parser(ABS_uri, index))
            SC_Excel_Table_Content(id,excel_id,table_content,excel_dict['经营']['name'],excel_dict['经营']['code']).add()
        if sheet.name.find("损益") != -1:
            GenSY(sheet,id)
            table_content = base64.b64encode(parseExcelToHtml.parser(ABS_uri, index))
            SC_Excel_Table_Content(id,excel_id,table_content,excel_dict['损益']['name'],excel_dict['损益']['code']).add()
        if sheet.name.find("交叉") != -1:
            GenJC(sheet,id)
            table_content = base64.b64encode(parseExcelToHtml.parser(ABS_uri, index))
            SC_Excel_Table_Content(id,excel_id,table_content,excel_dict['交叉']['name'],excel_dict['交叉']['code']).add()
        if sheet.name.find("点货") != -1:
            GenDH(sheet,id)
            table_content = base64.b64encode(parseExcelToHtml.parser(ABS_uri, index))
            SC_Excel_Table_Content(id,excel_id,table_content,excel_dict['点货']['name'],excel_dict['点货']['code']).add()
        if sheet.name.find("固资") != -1:
            GenGDZC(sheet,id)
            table_content = base64.b64encode(parseExcelToHtml.parser(ABS_uri, index))
            SC_Excel_Table_Content(id,excel_id,table_content,excel_dict['固资']['name'],excel_dict['固资']['code']).add()
        # if sheet.name.find("应收") != -1:
            # GenYS(sheet,self.dbHelp,id)
        # if sheet.name.find("应付") != -1:
            # GenYF(sheet,self.dbHelp,id)
        if sheet.name.find("道德品质") != -1:
            GenDDPZ(sheet,cert_no)
        if sheet.name.find("生存状况") != -1:
            GenSCZK(sheet,cert_no)
        if sheet.name.find("经营状况") != -1:
            GenJYZK(sheet,cert_no)

#执行sql
def executeSql(sql):
    sql = sql.replace("\\","")
    db.session.execute(sql)
    return int(db.session.execute("SELECT LAST_INSERT_ID()").fetchone()[0])
    
#目标客户        
def GenTargetCustomer(sheet):
    #keyMap = ["3-1","5-5","4-1","5-1"]
    customer_name = sheet.row(3)[1].value
    mobile = sheet.row(5)[5].value
    sex = 1
    if sheet.row(4)[1].value == "男":
        sex = 1
    elif sheet.row(4)[1].value == "女":
        sex = 0
    elif int(sheet.row(4)[1].value) == 2:
        sex = 0
    address = sheet.row(5)[1].value
    genSql = sql.sqlTargetCustomer.substitute(customer_name=customer_name,mobile=mobile,sex=sex,address=address)
    return executeSql(genSql)

# 个人客户表
def GenIndividualCustomer(sheet,customer_no):
    #keyMap = ["3-1","4-1","4-5","5-5","8-1","5-1","5-1"]
    customer_name = sheet.row(3)[1].value
    sex = 1
    if sheet.row(4)[1].value == "男":
        sex = 1
    elif sheet.row(4)[1].value == "女":
        sex = 0
    elif int(sheet.row(4)[1].value) == 2:
        sex = 0
    credentials_no = sheet.row(4)[5].value
    mobile = sheet.row(5)[5].value
    
    # 户籍所在地所在行不确定
    nrows = sheet.nrows #行数
    ncolnames = len(sheet.row_values(0)) #列数
    for rownum in range(0,13):
        row = sheet.row_values(rownum)
        if row:
            for i in range(ncolnames):
                if row[i] == "户籍所在地":
                    residence = row[i+1]
                    residence_address = row[i+1]
            
    home_address = sheet.row(9)[1].value
    genSql = sql.sqlIndividualCustomer.substitute(customer_no=customer_no,customer_name=customer_name,
        sex=sex,credentials_no=credentials_no,mobile=mobile,residence=residence,
        residence_address=residence_address,home_address=home_address)
    return executeSql(genSql)
    
#进件表
def Genrcs_application_info(sheet,customer_id,id):
    customer_name = sheet.row_values(3)[1]
    credentials_no = sheet.row(4)[5].value
    
    # 申请信息所在行不确定
    nrows = sheet.nrows #行数
    for rownum in range(0,nrows):
        row = sheet.row_values(rownum)
        if row[0] == "申请信息":
            loan_amount_num = sheet.row_values(rownum+1)[1]
            break
        
    genSql = sql.sql_rcs_application_info.substitute(customer_id=customer_id,customer_name=customer_name,card_id=credentials_no,
         loan_id=id,approve_je=loan_amount_num,create_user=current_user.id,create_time=datetime.datetime.now())
    return executeSql(genSql)
    
#贷款申请主表                
def GenLoanApply(sheet,customer_id):
    #keyMap = ["3-1"]
    customer_name = sheet.row_values(3)[1]
    genSql = sql.sqlLoanApply.substitute(belong_customer_value=customer_id,customer_name=customer_name)
    return executeSql(genSql)

# 申请信息表
def GenApplyInfo(sheet,id):
    # 申请信息所在行不确定
    nrows = sheet.nrows #行数
    for rownum in range(0,nrows):
        row = sheet.row_values(rownum)
        if row[0] == "申请信息":
            loan_amount_num = sheet.row_values(rownum+1)[1]
            loan_deadline = sheet.row_values(rownum+1)[4]
            details = sheet.row_values(rownum+2)[4].replace("\\","")
            break
    genSql = sql.sqlApplyInfo.substitute(loan_apply_id=id,loan_amount_num=loan_amount_num,loan_deadline=loan_deadline,details=details)
    return executeSql(genSql)
    
# 其他信息
def GenOthers(sheet,id):
    #从共同借款人开始出现不对齐的情况
    #所以用关键字"共同借款人"查找
    nrows = sheet.nrows #行数
    for rownum in range(0,nrows):
        row = sheet.row_values(rownum)
        if row[0] == "信贷历史":
            GenCreditHistory(sheet,id,rownum)
        if row[0] == "共同借款人":
            GenCoBrorrower(sheet,id,rownum)
        if row[0] == "担保人":
            GenGuarantees(sheet,id,rownum)
        if row[0] == "建议抵押物":
            GenGuaranty(sheet,id,rownum)
    
# 信贷历史表
def GenCreditHistory(sheet,id,rownum):
    #keyMap = ["18-0","18-1","18-2","18-3","18-4","18-5","18-6","18-7"]
    financing_sources = sheet.row_values(rownum+3)[0]
    loan_amount = sheet.row_values(rownum+3)[1]
    deadline = sheet.row_values(rownum+3)[2]
    use = sheet.row_values(rownum+3)[3]
    temp = sheet.row(rownum+3)[4].value
    if re.match(sql.datePattern, str(temp)) is None:
        release_date = '2013-01-01'
    else:
        release_date = sheet.row(rownum+3)[4].value
    overage = sheet.row_values(rownum+3)[5]
    guarantee = sheet.row_values(rownum+3)[6]
    late_information = sheet.row_values(rownum+3)[7]
        
    genSql = sql.sqlCreditHistory.substitute(loan_apply_id=id,financing_sources=financing_sources,loan_amount=loan_amount,
                deadline=deadline,use=use,release_date=release_date,overage=overage,guarantee=guarantee,late_information=late_information)
    executeSql(genSql)
    
# 共同借款人
def GenCoBrorrower(sheet,id,rownum):
    #keyMap = ["?-0","?-1","?-2","?-3","?-4","?-5","?-6","?-7"]
    name = sheet.row_values(rownum+2)[0]
    relationship = sheet.row_values(rownum+2)[1]
    id_number = sheet.row_values(rownum+2)[2]
    phone = sheet.row_values(rownum+2)[3]
    main_business = sheet.row_values(rownum+2)[6]
    address = sheet.row_values(rownum+2)[5]
    monthly_income = sheet.row_values(rownum+2)[7]
    home_addr = sheet.row_values(rownum+3)[1]
    
    genSql = sql.sqlCoBrorrower.substitute(loan_apply_id=id,name=name,relationship=relationship,id_number=id_number,
                phone=phone,main_business=main_business,address=address,monthly_income=monthly_income,home_addr=home_addr)
    executeSql(genSql)

# 担保人
def GenGuarantees(sheet,id,rownum):
    #keyMap = ["?-0","?-1","?-2","?-3","?-4","?-5","?-6","?-7"]
    name = sheet.row_values(rownum+2)[0]
    address = sheet.row_values(rownum+3)[1]
    id_number = sheet.row_values(rownum+2)[2]
    workunit = sheet.row_values(rownum+2)[5]
    phone = sheet.row_values(rownum+2)[4]
    relationship = sheet.row_values(rownum+2)[1]
    major_assets = sheet.row_values(rownum+2)[6]
    monthly_income = sheet.row_values(rownum+2)[7]
    home_addr = sheet.row_values(rownum+3)[1]
    hj_addr = sheet.row_values(rownum+3)[6]
    genSql = sql.sqlGuarantees.substitute(loan_apply_id=id,name=name,address=address,id_number=id_number,workunit=workunit,phone=phone,
                relationship=relationship,major_assets=major_assets,monthly_income=monthly_income,home_addr=home_addr,hj_addr=hj_addr)
    executeSql(genSql)
    
# 抵押物
def GenGuaranty(sheet,id,rownum):
    #keyMap = ["?-0","?-1","?-2","?-3","?-4","?-5"]
    obj_name = sheet.row_values(rownum+2)[0]
    owner_address = sheet.row_values(rownum+2)[1]
    description = sheet.row_values(rownum+2)[2]
    registration_number = sheet.row_values(rownum+2)[3]
    appraisal = sheet.row_values(rownum+2)[4]
    mortgage = sheet.row_values(rownum+2)[5]
    genSql = sql.sqlGuaranty.substitute(loan_apply_id=id,obj_name=obj_name,owner_address=owner_address,description=description,
                registration_number=registration_number,appraisal=appraisal,mortgage=mortgage)
    executeSql(genSql)

# 资产负债表
def GenZCFZB(sheet,id):
    keyMapZCFZB_col_0 = '{"流动资产":8,"现金及银行存款":0,"应收账款":2,"预付账款":4,"存货和原材料":6,"固定资产":10,"其他资产":12,"资产总计":17,"流动比率":19}'
    keyMapZCFZB_col_2 = '{"短期负债":9,"应付账款":1,"预收账款":3,"短期贷款":5,"社会集资":7,"长期负债":11,"其他负债":13,"负债总计":15,"所有者权益":16,"负债和所有者权益总计":18,"负债率%":20,"速动比率":14}'
    #keyMapZCFZB_col_3 = ["表外资产负债情况及评价"]
    json_col_0 = json.loads(keyMapZCFZB_col_0)
    json_col_2 = json.loads(keyMapZCFZB_col_2)
    nrows = sheet.nrows #行数
    # 循环keyMapZCFZB_col_0
    index = -1
    for rownum in range(3,nrows):
        row = sheet.row_values(rownum)
        if json_col_0.has_key(row[0]):
            index = 0
            loan_type = json_col_0.get(row[0])
        else:
            index = index + 1
        genSql = sql.sqlZCFZB.substitute(loan_apply_id=id,loan_type=loan_type,items_name=row[0],index=index,content=row[1])
        executeSql(genSql)
    
    index = -1
    # 循环keyMapZCFZB_col_2
    for rownum in range(3,nrows):
        row = sheet.row_values(rownum)
        if json_col_2.has_key(row[2]):
            index = 0
            loan_type = json_col_2.get(row[2])
        else:
            index = index + 1
        genSql = sql.sqlZCFZB.substitute(loan_apply_id=id,loan_type=loan_type,items_name=row[2],index=index,content=row[3])
        executeSql(genSql)
        if(loan_type == 6):
            #excel里没有社会集资 故 加上一条 保证页面不错乱
            genSql = sql.sqlZCFZB.substitute(loan_apply_id=id,loan_type=7,items_name='',index=index,content='')
            executeSql(genSql)
    
    
        
# 资产负债表(经营部分)
def GenJY(sheet,id):
    keyMap = ["1-0-1-1-21-经营历史和资本积累","2-0-2-1-22-生意现状（组织架构和市场）","3-0-3-1-23-生意现状（财务）",
            "4-1-4-2-26-自从上次申请后经营变化（重复贷款）生意方面","4-3-4-4-27-自从上次申请后经营变化（重复贷款）个人方面",
            "5-1-5-2-28-过去12个月的投资情况生意方面","5-3-5-4-29-过去12个月的投资情况个人方面",
            "6-1-6-2-31-未来12个月的投资计划生意方面","6-3-6-4-32-未来12个月的投资计划个人方面",
            "7-0-7-1-30-贷款目的详细描述","8-0-8-1-24-客户家庭状况（如房、车）",
            "9-0-9-1-25-对客户的印象","10-0-10-1-33-其他还款来源分析"]
    for obj in keyMap:
        obj_arr = obj.split("-")
        loan_type = obj_arr[4]
        items_name = obj_arr[5]
        try:
            content=sheet.row_values(int(obj_arr[2]))[int(obj_arr[3])]
        except Exception,ex:
            content=''
        genSql = sql.sqlZCFZB.substitute(loan_apply_id=id,loan_type=loan_type,items_name=items_name,index=0,content=content)
        executeSql(genSql)
    
# 损益表
def GenSY(sheet,id):
    keyMap = ["收入","可变成本","营业费用"]
    endFlag = False
    
    items_type = 0
    nrows = sheet.nrows #行数
    ncolnames = len(sheet.row_values(0)) #列数
        
    for rownum in range(2,nrows):# 从第二行开始
        index = 0
        row = sheet.row_values(rownum)
        
        if endFlag:
            break;
        if row[0] == "每月可支配资金":
            endFlag = True
            
        items_name = ""
        if row[1] != "":
            index = 0
            items_name = row[1]
        else:
            if row[0] in keyMap:
                items_type = items_type + 1
                continue
            else:
                index = index + 1
                items_name = row[0]
                
        if ncolnames < 16:#不满16列时
            nmonths = ncolnames - 4#减掉前后固定的4列
            for i in range(1,nmonths+1):
                exec("month_%d = row[%d]" % (i,i+1))
            for i in range(nmonths+1,13):
                exec("month_%d = None" % (i))
        else:
            for i in range(1,13):
                exec("month_%d = row[%d]" % (i,i+1))
        
        #for i in range(1,13):
        #    print eval("month_%d" % i)
        
        genSql = sql.sqlSY.substitute(loan_apply_id=id,items_type=items_type,items_name=items_name,index=index,
            month_1=month_1,month_2=month_2,month_3=month_3,month_4=month_4,month_5=month_5,month_6=month_6,
            month_7=month_7,month_8=month_8,month_9=month_9,month_10=month_10,month_11=month_11,month_12=month_12)    
        executeSql(genSql)
        
        items_type = items_type + 1
    
# 交叉检验
def GenJC(sheet,id):
    keyMap_1 = '{"销售额交叉检验":0,"毛利润/成本交叉检验":1,"其他交叉检验":2}'
    row_2 = 0#第二个map的开始行
    keyMap_2 = '{"期初权益合计":3,"分析期间收入合计":4,"大项支出合计":5,"其他收入":6,"升值":7,\
                "折旧":8,"表外资产":9,"应有权益":10,"实际权益（资产负债表所有者权益）":11,\
                "权益差额（应有权益-实际权益）":12,"分析期间累计收入":13,"权益交叉检验比率":14}'
    
    loan_type = 0
    nrows = sheet.nrows #行数
    # 循环kepMap_1
    json_keyMap_1 = json.loads(keyMap_1)
    for rownum in range(2,nrows):
        row = sheet.row_values(rownum)
        if row[0] in json_keyMap_1.keys():
            loan_type = json_keyMap_1.get(row[0])
            genSql = sql.sqlJC.substitute(loan_apply_id=id,loan_type=loan_type,items_name=row[0],index=0,content=sheet.row_values(rownum+1)[0])
            executeSql(genSql)
        if row[0].find("权益交叉检验") != -1:
            row_2 = rownum
            break
        
    loan_type = 0
    index = 0
    # 循环keyMap_2
    json_keyMap_2 = json.loads(keyMap_2)
    for rownum in range(row_2,nrows):
        row = sheet.row_values(rownum)
        if row[0] in json_keyMap_2.keys():
            index = 0
            loan_type = json_keyMap_2.get(row[0])
        else:
            index = index + 1
        genSql = sql.sqlJC.substitute(loan_apply_id=id,loan_type=loan_type,items_name=row[0],index=index,content=sheet.row_values(rownum)[1])
        executeSql(genSql)
            
# 点货
def GenDH(sheet,id):
    nrows = sheet.nrows #行数
    for rownum in range(3,nrows):
        row = sheet.row_values(rownum)
        genSql = sql.sqlDH.substitute(loan_apply_id=id,name=row[0],amount=row[1],purchase_price=row[2],purchase_total_price=row[3])
        executeSql(genSql)

# 固定资产
def GenGDZC(sheet,id):    
    nrows = sheet.nrows #行数
    for rownum in range(3,nrows):
        row = sheet.row_values(rownum)
        temp = row[2]
        if re.match(sql.datePattern, str(temp)) is None:
            purchase_date = '2013-01-01'
        else:
            purchase_date = row[2]
        genSql = sql.sqlGDZC.substitute(loan_apply_id=id,name=row[1],purchase_date=purchase_date,total_price=row[6],rate=row[4],total=row[5],rate_price=row[7],purchase_price=row[3])
        executeSql(genSql)
    
# 应收账款
def GenYS(sheet,id):
    nrows = sheet.nrows #行数
    for rownum in range(3,nrows):
        row = sheet.row_values(rownum)
        genSql = sql.sqlYSYF.substitute(loan_apply_id=id,name=row[1],original_price=row[4],occur_date=row[2],deadline=row[3],mode_type=2)
        executeSql(genSql)
        
# 应付账款    
def GenYF(sheet,id):
    nrows = sheet.nrows #行数
    for rownum in range(3,nrows):
        row = sheet.row_values(rownum)
        genSql = sql.sqlYSYF.substitute(loan_apply_id=id,name=row[1],original_price=row[4],occur_date=row[2],deadline=row[3],mode_type=1)
        executeSql(genSql)

# 道德品质
def GenDDPZ(sheet,cert_no):    
    nrows = sheet.nrows #行数
    value_2 = ""
    info = Rcs_Application_Info.query.filter_by(card_id=cert_no).first()
    for rownum in range(1,nrows):
        row = sheet.row_values(rownum)
        value_2 += row[2]+"@@"+row[3]+","
    value_2 = value_2[:-1]
    ddpz = Rcs_Application_Ddpz.query.filter_by(application_id=info.id).first()
    if ddpz:
        ddpz.value_2=value_2
    else:
        Rcs_Application_Ddpz(info.id,"",value_2).add()
    db.session.commit()

# 生存状况
def GenSCZK(sheet,cert_no):    
    nrows = sheet.nrows #行数
    value_2 = ""
    info = Rcs_Application_Info.query.filter_by(card_id=cert_no).first()
    for rownum in range(0,nrows):
        row = sheet.row_values(rownum)
        temp = row[0]
        value_2 += row[0]+"@@"+row[1]+","
    value_2 = value_2[:-1]
    shzk = Rcs_Application_Shzk.query.filter_by(application_id=info.id).first()
    if shzk:
        shzk.value_2=value_2
    else:
        Rcs_Application_Shzk(info.id,"",value_2).add()
    db.session.commit()

# 经营状况
def GenJYZK(sheet,cert_no):    
    nrows = sheet.nrows #行数
    value_2 = ""
    info = Rcs_Application_Info.query.filter_by(card_id=cert_no).first()
    for rownum in range(0,nrows):
        row = sheet.row_values(rownum)
        temp = row[0]
        value_2 += row[0]+"@@"+row[1]+","
    value_2 = value_2[:-1]
    jyzk = Rcs_Application_Jyzk.query.filter_by(application_id=info.id).first()
    if jyzk:
        jyzk.value_2=value_2
    else:
        Rcs_Application_Jyzk(info.id,"",value_2).add()
    db.session.commit()
    