# coding:utf-8
import hashlib

from RemoteCreditSystem import User
from RemoteCreditSystem.models import Org
from RemoteCreditSystem.models.system.Role import Role
from RemoteCreditSystem.models import UserRole,Rcs_Access_Right,Indiv_Brt_Place
from RemoteCreditSystem.models.system_usage.Rcs_Application_Info import Rcs_Application_Info
from RemoteCreditSystem.models.system_usage.Rcs_Application_Advice import Rcs_Application_Advice
from RemoteCreditSystem.models.system_usage.Rcs_Application_Score import Rcs_Application_Score
from RemoteCreditSystem.models.system_usage.Rcs_Application_Result import Rcs_Application_Result
from RemoteCreditSystem.models.system_usage.Rcs_Application_Xjll import Rcs_Application_Xjll
from RemoteCreditSystem.models.system_usage.Rcs_Application_Jcjy import Rcs_Application_Jcjy
from RemoteCreditSystem.models.system_usage.Rcs_Application_Zcfzb import Rcs_Application_Zcfzb
from RemoteCreditSystem.models.system_usage.Rcs_Application_Lrb import Rcs_Application_Lrb
from RemoteCreditSystem.models.system_usage.Rcs_Application_Jyzk import Rcs_Application_Jyzk
from RemoteCreditSystem.models.system_usage.Rcs_Application_Ddpz import Rcs_Application_Ddpz
from RemoteCreditSystem.models.system_usage.Rcs_Application_Expert import Rcs_Application_Expert
from RemoteCreditSystem.models.system_usage.Rcs_Application_Shzk import Rcs_Application_Shzk
from RemoteCreditSystem.models.system_usage.Rcs_Parameter import Rcs_Parameter
from RemoteCreditSystem.models.system_usage.Rcs_Expert_Information import Rcs_Expert_Information
from flask import request, render_template,flash,redirect,session
from flask.ext.login import login_user, logout_user, current_user, login_required
from RemoteCreditSystem import app
from RemoteCreditSystem import db
import datetime
from RemoteCreditSystem.config import Application_Type_Create,Application_Type_Approve,Application_Type_Finish
from RemoteCreditSystem.config import logger
from RemoteCreditSystem.config import PER_PAGE
import RemoteCreditSystem.helpers as helpers

from RemoteCreditSystem.tools.SimpleCache import SimpleCache

from RemoteCreditSystem.models import Rcs_Application_Log,Rcs_Application_Absent,Rcs_Expert_Refuse


#get md5 of a input string
def GetStringMD5(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()
    
# 登陆
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

# 注销
@app.route('/logout')
def logout():
    logout_user()
    return render_template("login.html")
    
# 心跳
@app.route('/heartBeat', methods=['GET'])
def heartBeat():
    if(session.has_key(str(current_user.id))):
        session[str(current_user.id)] = session[str(current_user.id)].split("_")[0]+"_"+str(datetime.datetime.now())
    else:
        session[str(current_user.id)] = str(datetime.datetime.now())+"_"+str(datetime.datetime.now())
        

    return helpers.show_result_success('') # 返回json

# 欢迎界面
@app.route('/doLogin', methods=['POST'])
def doLogin():
    user = User.query.filter_by(login_name=request.form['login_name'], login_password=GetStringMD5(request.form['login_password'])).first()
    if user:
        if(user.active =='0'):
            flash('该用户已被禁用，请联系管理员','error')
            return helpers.show_result_fail("")
        
        login_user(user)
        #设置session
        #heartBeat()
        return helpers.show_result_success("")
    else:
        flash('用户名或密码错误','error')
        return helpers.show_result_fail("")

# index
@app.route('/index', methods=['GET'])
@login_required
def index():
    simplecache = SimpleCache.getInstance()
    tree = []
    userrole = UserRole.query.filter_by(user_id=current_user.id).first()
    if userrole:
        role_id = userrole.role_id
        rcs_access_right = Rcs_Access_Right.query.filter_by(role_id=role_id).order_by("id").all()
        
        if(current_user.login_name == 'admin'):
            for key_cache in simplecache:
                obj_tmp = simplecache[key_cache]
                if(obj_tmp['levels'] == '2' or obj_tmp['levels'] == '3'):
                    tree.append(obj_tmp)
        else:
            for key_cache in simplecache:  
                obj_tmp = simplecache[key_cache]
                obj_tmp['checked'] = False
                for obj_access_right in rcs_access_right:
                    if(obj_tmp['levels'] != '4'): 
                        if(obj_tmp['id'] == obj_access_right.resource_id):
                            obj_tmp['checked'] = True
                            break;  
                    elif(obj_tmp['levels'] == '4'):
                        if(obj_tmp['id'].split("_")[0] == obj_access_right.resource_id):
                            if(int(obj_access_right.operations) & int(obj_tmp['id'].split("_")[1]) != 0):
                                obj_tmp['checked'] = True
                            break; 
                tree.append(obj_tmp)
                
            dellist = []
            for obj in tree:
                if(obj['levels'] == '1' or obj['levels'] == '4' or obj['checked'] == False):
                    dellist.append(obj)
            for obj in dellist:
                tree.remove(obj)
    return render_template("index.html",tree=tree)

# welcome
@app.route('/welcome', methods=['GET'])
def welcome():
    #显示角色
    role = Role.query.filter("id in (select role_id from rcs_userrole where user_id="+str(current_user.id)+")").first()
    list_wait=''
    len_wait=0
    list_allot=''
    len_allot=0
    list_access=''
    len_access=0
    #客户经理
    if current_user.user_type=='3':
        list_wait = Rcs_Application_Info.query.filter("create_user="+str(current_user.id)+" and approve_type in (1,2)").all()
        len_wait =len(list_wait)
        if len_wait>10:
            list_wait = list_wait[0:10]
    #专家
    elif current_user.user_type=='1':
        list_wait = Rcs_Application_Info.query.filter("approve_type='2' and id in (select application_id from rcs_application_expert where expert_id="+str(current_user.id)+" and operate='0')").all()
        len_wait =len(list_wait)
        if len_wait>10:
            list_wait = list_wait[0:10]
    #决策岗
    else:
        #待授信
        list_wait = Rcs_Application_Info.query.all()
        len_wait =len(list_wait)
        if len_wait>10:
            list_wait = list_wait[0:10]
        #待分配
        list_allot = Rcs_Application_Info.query.filter("id in (select loan_apply_id from sc_excel_table_content)").all()
        len_allot =len(list_allot)
        if len_allot>10:
            list_allot = list_wait[0:10]
        #待最终评估
        sql = " id in (select application_id from rcs_application_expert where application_id not in (SELECT application_id FROM rcs_application_expert where operate =0))  GROUP BY id"
        list_access = Rcs_Application_Info.query.filter(sql).all()
        len_access = len(list_access)
        if len_access>10:
            list_access = list_access[0:10]
    #获取机构
    org=''
    if current_user.org_id:
        org = Org.query.filter_by(id=current_user.org_id).first().org_name
    else:
        #递归获取上级用户机构
        org = reGetOrg(current_user.pId)
    return render_template("welcome.html",list_wait=list_wait,len_wait=len_wait,list_allot=list_allot,len_allot=len_allot,list_access=list_access,len_access=len_access,current_user=current_user,role=role,org=org)
#递归查询上级用户机构
def reGetOrg(pId):
    user = User.query.filter_by(id=pId).first()
    if user.org_id:
        org = Org.query.filter_by(id=user.org_id).first()
        return org.org_name
    else:
        reGetOrg(user.pId)

# 修改密码
@app.route('/change_password/<int:id>', methods=['GET','POST'])
def change_password(id):
    if request.method == 'POST':
        try:
            user = User.query.filter_by(id=id).first()
            if user.login_password == GetStringMD5(request.form['old_password']):
                user.login_password = GetStringMD5(request.form['login_password'])
            else:
                raise Exception

            # 事务提交
            db.session.commit()
            # 消息闪现
            flash('修改密码成功，请重新登录！','success')

        except:
            # 回滚
            db.session.rollback()
            logger.exception('exception')
            # 消息闪现
            flash('修改密码失败，为保障账号安全，请重新登录后再尝试修改！','error')

        logout_user()
        return redirect("login")
    else:
        return render_template("change_password.html")
    
@app.route('/jjrwfa/zxpg', methods=['GET'])
@login_required
def zxpg():        
    return render_template("jjrwfa/zxpg.html")

#进件分案页面
@app.route('/jjrwfa/jjfa/<int:page>', methods=['GET','POST'])
@login_required
def jjfa(page):
    sql=" approve_type="+str(Application_Type_Create)
    if str(current_user.user_type)!='2':
        sql+=" and create_user="+str(current_user.id)
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        card_id = request.form['card_id']
        if customer_name:
            sql+=" and customer_name like '%"+customer_name+"%'"
        if card_id:
            sql+=" and card_id='"+card_id+"'"    
    #获取未分类数据   
    appList = Rcs_Application_Info.query.filter(sql).paginate(page, per_page = PER_PAGE)
    count = len(Rcs_Application_Info.query.filter(sql).all())
    return render_template("jjrwfa/jjfa.html",appList=appList,current_user=current_user,count=count)

@app.route('/jjrwfa/jjrwfaxx', methods=['GET'])
@login_required
def jjrwfaxx():        
    return render_template("jjrwfa/jjrwfaxx.html")

@app.route('/jjrwfa/zxpgmsgzwh', methods=['GET'])
@login_required
def zxpgmsgzwh():        
    return render_template("jjrwfa/zxpgmsgzwh.html")

@app.route('/jjrwfa/fagzwh', methods=['GET'])
@login_required
def fagzwh():        
    return render_template("jjrwfa/fagzwh.html")

@app.route('/jjrwfa/zxpgzjhsgzwh', methods=['GET'])
@login_required
def zxpgzjhsgzwh():        
    return render_template("jjrwfa/zxpgzjhsgzwh.html")

#进入新增进件页面
@app.route('/jjrwfa/new_jjfa', methods=['GET'])
def new_jjfa():        
    return render_template("jjrwfa/new_jjfa.html")

#ajax判断身份证是否重复
@app.route('/jjrwfa/new_jjfa_check/<card_id>', methods=['GET'])
def new_jjfa_check(card_id):
    info = Rcs_Application_Info.query.filter_by(card_id=card_id).first()
    if info:
        return 'true'
    else:
        return 'false'

#新增进件保存页面
@app.route('/jjrwfa/save_jjfa', methods=['POST'])
def save_jjfa():
    try:
        name = request.form['name']
        card_id = request.form['card_id']
        index_id = request.form['index_id']
        bank_id = request.form['bank_id']
        place_all = ''
        place_all_name = ''
        #联动1
        regPermResidence_1 = request.form['regPermResidence_1']
        indiv = Indiv_Brt_Place.query.filter_by(type_code=regPermResidence_1.split('_')[1]).first()
        place_all_name+=indiv.type_name
        place_all+=regPermResidence_1.split('_')[1]
        place = Indiv_Brt_Place.query.filter_by(parent_code=regPermResidence_1.split('_')[1]).first()
        if place:
            #联动2
            regPermResidence_2 = request.form['regPermResidence_2']
            indiv_1 = Indiv_Brt_Place.query.filter_by(type_code=regPermResidence_2.split('_')[1]).first()
            place_all+="|"+regPermResidence_2.split('_')[1]
            place_all_name+=indiv_1.type_name
            place_2 = Indiv_Brt_Place.query.filter_by(parent_code=regPermResidence_2.split('_')[1]).first()
            if place_2:
                regPermResidence_3 = request.form['regPermResidence_3']
                indiv_2 = Indiv_Brt_Place.query.filter_by(type_code=regPermResidence_3.split('_')[1]).first()
                place_all+="|"+regPermResidence_3.split('_')[1]
                place_all_name+=indiv_2.type_name
 
        org_id = request.form['org_id']
        industry_id = request.form['industry_id']
        district_id = request.form['district_id']
        product_id = request.form['product_id']
        approve_limit = request.form['approve_limit']
        manager_id = request.form['manager_id']
        sh_user = request.form['sh_user']
        sp_user = request.form['sp_user']
        #进件状态为1
        approve_type = '1'
        #进件模型类型,未定义
        model_type=0
        Rcs_Application_Info(index_id,name,card_id,product_id,approve_limit,org_id,place_all_name,place_all,industry_id,district_id,manager_id,sh_user,sp_user,approve_type,model_type,None).add()
        db.session.commit()
        # 消息闪现
        flash('保存成功','success')
    except:
        # 回滚
        db.session.rollback()
        logger.exception('exception')
        # 消息闪现
        flash('保存失败','error')

    return redirect("/jjrwfa/jjfa/1")
#人工分案
@app.route('/jjrwfa/rgfa/<int:userId>', methods=['GET'])
def rgfa(userId):        
    app = Rcs_Application_Info.query.filter_by(id=userId).first()  
    #选择所有专家
    users = User.query.filter_by(user_type='1').all()
    return render_template("jjrwfa/rgfa.html",app=app,users=users)

@app.route('/jjrwfa/xtfa', methods=['GET'])
def xtfa():        
    return render_template("jjrwfa/xtfa.html")

@app.route('/jjrwfa/show_jjfa/<int:userId>', methods=['GET'])
def show_jjfa(userId):  
    app = Rcs_Application_Info.query.filter_by(id=userId).first()   
    return render_template("jjrwfa/show_jjfa.html",app=app)

@app.route('/jjrwfa/insert_jjfa/<int:id>/<expertId>/<int:hours>', methods=['GET'])
def insert_jjfa(id,expertId,hours):  
    app = Rcs_Application_Info.query.filter_by(id=id).first()   
    app.approve_type=Application_Type_Approve
    app.create_time = datetime.datetime.now()
    app.effect_time = datetime.datetime.now()+datetime.timedelta(hours=hours)
    ids = expertId.split(",")
    for obj in ids:
        Rcs_Application_Expert(id,int(obj)).add()
    db.session.commit()
    flash('保存成功','success')
    return redirect("/jjrwfa/jjfa/1")


@app.route('/mxpg/pldr/<int:page>', methods=['GET','POST'])
@login_required
def pldr(page):     
    sql=" approve_type="+str(Application_Type_Create)
    sql+=" and create_user="+str(current_user.id)
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        card_id = request.form['card_id']
        if customer_name:
            sql+=" and customer_name like '%"+customer_name+"%'"
        if card_id:
            sql+=" and card_id='"+card_id+"'"    
    #获取未分类数据   
    appList = Rcs_Application_Info.query.filter(sql).paginate(page, per_page = PER_PAGE)
    count = len(Rcs_Application_Info.query.filter(sql).all())
    return render_template("mxpg/pldr.html",appList=appList,count=count)

@app.route('/mxpg/xxlr/<int:page>', methods=['GET','POST'])
@login_required
def xxlr(page):
    sql=" create_user="+str(current_user.id)
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        card_id = request.form['card_id']
        if customer_name:
            sql+=" and customer_name like '%"+customer_name+"%'"
        if card_id:
            sql+=" and card_id='"+card_id+"'"
    #获取未分类数据   
    appList = Rcs_Application_Info.query.filter(sql).paginate(page, per_page = PER_PAGE)
    length = len(Rcs_Application_Info.query.filter(sql).all())
    for obj in appList.items:
        if not obj.model_type:
            obj.model_type="0"
    return render_template("mxpg/xxlr.html",appList=appList,length=length)

#授信评估
@app.route('/mxpg/sxpg/<int:page>', methods=['GET','POST'])
@login_required
def sxpg(page): 
    sql = "approve_type in (1,2)"
    customer_name=''
    card_id=''
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        card_id = request.form['card_id']
        if customer_name:
            sql+=" and customer_name like '%"+customer_name+"%'"
        if card_id:
            sql+=" and card_id='"+card_id+"'"
    #获取未分类数据     
    appList = Rcs_Application_Info.query.filter(sql).paginate(page, per_page = PER_PAGE)   
    count = len(Rcs_Application_Info.query.filter(sql).all())
    return render_template("mxpg/sxpg.html",appList=appList,customer_name=customer_name,card_id=card_id,count=count)

#评估报告
@app.route('/mxpg/pgbg/<int:page>', methods=['GET','POST'])
@login_required
def pgbg(page):   
    sql = "1=1"
    customer_name=''
    card_id=''
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        card_id = request.form['card_id']
        if customer_name:
            sql+=" and customer_name like '%"+customer_name+"%'"
        if card_id:
            sql+=" and card_id='"+card_id+"'"   
    #获取未分类数据     
    appList = Rcs_Application_Info.query.filter(sql).paginate(page, per_page = PER_PAGE)
    count = len(Rcs_Application_Info.query.filter(sql).all())
    return render_template("mxpg/pgbg.html",appList=appList,customer_name=customer_name,card_id=card_id,count=count)


#参数管理
@app.route('/mxpg/csgl', methods=['GET'])
@login_required
def csgl():  
    return render_template("mxpg/csgl.html")

#参数配置--进入iframe
@app.route('/mxpg/iframe_cspz', methods=['GET'])
def iframe_cspz():    
    return render_template("mxpg/iframe_cspz.html")



#参数配置--还款能力
@app.route('/mxpg/cspz_hknl', methods=['GET'])
def cspz_hknl():   
    hknl = Rcs_Parameter.query.filter_by(parameter_name="hknl").first()
    result = ""
    if hknl:
        result=hknl.parameter_value 
    return render_template("mxpg/cspz_hknl.html",result=result)

#参数配置--还款能力--保存
@app.route('/mxpg/cspz_hknl_save/<score>', methods=['GET'])
def cspz_hknl_save(score):
    try:
        Rcs_Parameter.query.filter_by(parameter_name="hknl").delete()
        Rcs_Parameter("hknl",score).add()
        db.session.commit()
    # 消息闪现
        flash('保存成功','success')
    except:
        # 回滚
        db.session.rollback()
        logger.exception('exception')
        # 消息闪现
        flash('保存失败','error')
    return redirect("/mxpg/cspz_hknl")

#客户资料
@app.route('/khzldy/khzl/<int:page>', methods=['GET','POST'])
@login_required
def khzl(page):      
    sql=" create_user="+str(current_user.id)
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        card_id = request.form['card_id']
        if customer_name:
            sql+=" and customer_name like '%"+customer_name+"%'"
        if card_id:
            sql+=" and card_id='"+card_id+"'"    
    #获取未分类数据   
    appList = Rcs_Application_Info.query.filter(sql).paginate(page, per_page = PER_PAGE)
    count = len(Rcs_Application_Info.query.filter(sql).all())
    return render_template("khzldy/khzl.html",appList=appList,count=count)

#还款能力页面(iframe)
@app.route('/khzldy/khzl_hknl/<type>/<int:id>', methods=['GET'])
def khzl_hknl(type,id):        
    return render_template("customer/iframe.html",id=id,type=type)

#还款能力页面
@app.route('/khzldy/khzl_hk/<int:id>', methods=['GET'])
def khzl_hk(id):   
    hknl = Rcs_Parameter.query.filter_by(parameter_name="hknl").first()
    result=hknl.parameter_value     
    #获取还款结果
    appResult = Rcs_Application_Result.query.filter_by(application_id=id).first()  
    if not appResult:
        appResult = Rcs_Application_Result(id,"","","","","","","","","").add()
    db.session.commit()
    appResult = Rcs_Application_Result.query.filter_by(application_id=id).first()
    #获取交叉检验结果
    jcjy = Rcs_Application_Jcjy.query.filter_by(application_id=id).first()

    return render_template("customer/hknl.html",result=result,id=id,appResult=appResult,jcjy=jcjy)



@app.route('/zjzxpggl/jjrw', methods=['GET'])
@login_required
def jjrw(): 
    #获取进件任务数据  
    appList = Rcs_Application_Info.query.filter("approve_type='2' and id in (select application_id from rcs_application_expert where expert_id="+str(current_user.id)+")").all()
    return render_template("zjzxpggl/jjrw.html",appList=appList)

#评估任务
@app.route('/zjzxpggl/yjsrw/<int:page>', methods=['GET','POST'])
@login_required
def yjsrw(page):
    sql="approve_type='2' and id in (select application_id from rcs_application_expert where expert_id="+str(current_user.id)+")"
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        card_id = request.form['card_id']
        if customer_name:
            sql+=" and customer_name like '%"+customer_name+"%'"
        if card_id:
            sql+=" and card_id='"+card_id+"'"  
    appList = Rcs_Application_Info.query.filter(sql).paginate(page, per_page = PER_PAGE)
    count = len(Rcs_Application_Info.query.filter(sql).all())
    return render_template("zjzxpggl/yjsrw.html",appList=appList,count=count)

#拒绝任务
@app.route('/zjzxpggl/refuse', methods=['GET','POST'])
def refuse():
    try:
        id = request.form['hiddenId']
        refuse_reason = request.form['refuse_reason']
        #删除进件关系表
        Rcs_Application_Expert.query.filter_by(application_id=id,expert_id=current_user.id).delete()
        db.session.flush()
        info = Rcs_Application_Info.query.filter_by(id=id).first()
        Rcs_Expert_Refuse(current_user.id,current_user.real_name,id,info.customer_name,refuse_reason,None,'').add()
        db.session.commit()
    # 消息闪现
        flash('拒绝成功','success')
    except:
        # 回滚
        db.session.rollback()
        logger.exception('exception')
        # 消息闪现
        flash('拒绝失败','error')
    return redirect("zjzxpggl/yjsrw/1")

#拒绝任务记录查看
@app.route('/zjzxpggl/has_refuse/<int:page>', methods=['GET','POST'])
@login_required
def has_refuse(page):
    sql = "1=1"
    if request.method == 'POST':
        application_name = request.form['customer_name']
        expert_name = request.form['expert_name']
        if application_name:
            sql+=" and application_name like '%"+application_name+"%'"
        if expert_name:
            sql+=" and expert_name like '%"+expert_name+"%'"
    appList = Rcs_Expert_Refuse.query.filter(sql).paginate(page, per_page = PER_PAGE)
    count = len(Rcs_Expert_Refuse.query.filter(sql).all())
    return render_template("zjzxpggl/refuse_list.html",appList=appList,count=count)

#拒绝任务重分配保存
@app.route('/zjzxpggl/has_refuse_save', methods=['POST'])
def has_refuse_save():
    try:
        id = request.form['hiddenId']
        expert_id = request.form['expert']
        refuse = Rcs_Expert_Refuse.query.filter_by(id=id).first()
        users = User.query.filter_by(id=expert_id).first()
        refuse.new_expert_id = expert_id
        refuse.new_expert_name = users.real_name
        #进件关系表添加记录
        Rcs_Application_Expert(refuse.application_id,expert_id).add()
        db.session.commit()
    # 消息闪现
        flash('重分配成功','success')
    except:
        # 回滚
        db.session.rollback()
        logger.exception('exception')
        # 消息闪现
        flash('重分配失败','error')
    return redirect("/zjzxpggl/has_refuse/1")

#判断是否已重分配
@app.route('/zjzxpggl/restart/<refuse_id>', methods=['GET'])
def restart(refuse_id):
    refuse = Rcs_Expert_Refuse.query.filter_by(id=refuse_id).first()
    if refuse.new_expert_id:
        return "true"
    else:
        return "false"

#评估结论记录查看
@app.route('/zxpgjl/pgjl/<int:page>', methods=['GET','POST'])
@login_required
def pgjl(page):
    sql = "approve_type in (2,3)"
    #客户经理
    if current_user.user_type=='3':
        sql+=" and create_user="+str(current_user.id)
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        card_id = request.form['card_id']
        if customer_name:
            sql+=" and customer_name like '%"+customer_name+"%'"
        if card_id:
            sql+=" and card_id='"+card_id+"'"  
    appList = Rcs_Application_Info.query.filter(sql).paginate(page, per_page = PER_PAGE)
    count = len(Rcs_Application_Info.query.filter(sql).all())
    return render_template("zxpgjl/pgjl.html",appList=appList,count=count)
#评估结果
@app.route('/zxpgjl/pgjl_info/<int:id>', methods=['GET'])
def pgjl_info(id):        
    app = Rcs_Application_Info.query.filter_by(id=id).first()
    #评估建议
    advice = Rcs_Application_Advice.query.filter_by(application_id=id,advice_type=1).all()
    #未评估专家
    expert = Rcs_Application_Expert.query.filter("application_id="+str(id)+" and expert_id not in (select user_id from rcs_application_advice where application_id="+str(id)+")").all()
    #最终决策人员建议
    last_advice = Rcs_Application_Advice.query.filter_by(application_id=id,advice_type=2).first()
    #获取模型审批额度
    score = Rcs_Application_Score.query.filter_by(application_id=id).first()
    return render_template("zxpgjl/pgjl_info.html",app=app,advice=advice,expert=expert,level=current_user.user_type,last_advice=last_advice,score=score)

#最终决策人员评估保存
@app.route('/zxpgjl/save_pgjl_info/<int:id>', methods=['POST'])
def save_pgjl_info(id):
    try:
        info = Rcs_Application_Info.query.filter_by(id=id).first()
        last_advice = request.form['last_advice']
        last_approve = request.form['last_approve']
        approve_advice = request.form['advice_end']
        advice = Rcs_Application_Advice.query.filter_by(application_id=id,user_id=current_user.id).first()
        if advice:
            advice.approve_result = last_advice
            advice.approve_ed = last_approve
        else:
            Rcs_Application_Advice(id,approve_advice,last_advice,last_approve,"2").add()
        #进件标志
        info.approve_type=Application_Type_Finish
        #保存进件日志
        Rcs_Application_Log(id,info.customer_id,info.customer_name,last_advice,last_approve).add()
        #保存缺席专家日志
        #未评估专家
        expert = Rcs_Application_Expert.query.filter("application_id="+str(id)+" and expert_id not in (select user_id from rcs_application_advice where application_id="+str(id)+")").all()
        for obj in expert:
            Rcs_Application_Absent(id,info.card_id,info.customer_name,obj.expert_id,obj.rcs_expert_ibfk_1.real_name).add()
        db.session.commit()
        flash('保存成功','success')
    except:
        # 回滚
        db.session.rollback()
        logger.exception('exception')
        # 消息闪现
        flash('保存失败','error')
    return redirect("/zxpgjl/pgjl_info/"+str(id))

#撤销专家页面
@app.route('/zxpgjl/cancel/<int:id>', methods=['GET'])
def cancel(id):        
    app = Rcs_Application_Info.query.filter_by(id=id).first()
    #评估建议
    advice = Rcs_Application_Advice.query.filter_by(application_id=id,advice_type=1).all()
    #未评估专家
    experts = Rcs_Application_Expert.query.filter("application_id="+str(id)+" and expert_id not in (select user_id from rcs_application_advice where application_id="+str(id)+")").all()

    return render_template("zxpgjl/pgjl_cancel.html",app=app,advice=advice,experts=experts)

#撤销专家保存
@app.route('/zxpgjl/cancel_save/<int:id>', methods=['POST'])
def cancel_save(id):
    try:
        #删除未评估专家
        Rcs_Application_Expert.query.filter_by(application_id=id,operate=0).delete()
        db.session.flush()
        #重新保存评估专家
        expertId = request.form.getlist('expert')
        for obj in expertId:
            #判断是否重复
            expert = Rcs_Application_Expert.query.filter_by(application_id=id,expert_id=obj).first()
            if not expert:
                Rcs_Application_Expert(id,int(obj)).add()
        db.session.commit()
        flash('撤销成功','success')
    except:
        # 回滚
        db.session.rollback()
        logger.exception('exception')
        # 消息闪现
        flash('撤销失败','error')
    return redirect("/zxpgjl/pgjl_info/"+str(id))


@app.route('/zxpggzwh/pggzwh', methods=['GET'])
@login_required
def pggzwh():        
    return render_template("zxpggzwh/pggzwh.html")

#专家信息管理
@app.route('/pgzjgl/zjxxgl/<int:page>', methods=['GET','POST'])
@login_required
def zjxxgl(page):
    sql="(user_type='1' or user_type='2')"
    customer_name=''
    card_id=''
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        card_id = request.form['card_id']
        if customer_name:
            sql+=" and real_name like '%"+customer_name+"%'"
        if card_id:
            sql+=" and card_id='"+card_id+"'"  
			
    #获取专家信息 
    user = User.query.filter(sql).paginate(page, per_page = PER_PAGE)
    count =len(User.query.filter(sql).all())       
    return render_template("pgzjgl/zjxxgl.html",user=user,count=count,customer_name=customer_name,card_id=card_id)
	
#新增
@app.route('/pgzjgl/new_zjxxgl', methods=['GET'])
def new_zjxxgl():  
    return render_template("pgzjgl/new_zjxxgl.html")

#新增保存
@app.route('/pgzjgl/new_zjxxgl_save', methods=['POST'])
def new_zjxxgl_save():    
    try:
        user_name = request.form['user_name']   
        sex = request.form['sex']   
        card_id = request.form['card_id']   
        phone = request.form['phone']   
        level = request.form['level']
        org = request.form['org']

        address = request.form['address']
        hy = request.form['hy']
        qy = request.form['qy']
        product = request.form['product']
        balance = request.form['balance']
        zyzc = request.form['zyzc']
        xrzw = request.form['xrzw']
        expert_level = request.form['expert_level']
        approve_role = request.form['approve_role']
        gzr = request.form['gzr']
        gzsd = request.form['gzsd']
        user = User(user_name,GetStringMD5('111111'),user_name,sex,phone,1,'',card_id,level,org,None)
        user.add()
        db.session.flush()
        Rcs_Expert_Information(user.id,address,hy,qy,product,balance,zyzc,xrzw,expert_level,approve_role,gzr,gzsd).add() 
        db.session.commit()
        flash('保存成功','success')
    except:
        # 回滚
        db.session.rollback()
        logger.exception('exception')
        # 消息闪现
        flash('保存失败','error')
    return redirect('/pgzjgl/zjxxgl/1')

#修改页面
@app.route('/pgzjgl/edit_zjxxgl/<int:id>', methods=['GET'])
def edit_zjxxgl(id):    
    #获取专家信息 
    user = User.query.filter_by(id=id).first()
    user_information = Rcs_Expert_Information.query.filter_by(expert_id=id).first()
    return render_template("pgzjgl/edit_zjxxgl.html",user=user,user_information=user_information)
#修改提交
@app.route('/pgzjgl/edit_zjxxgl_save/<int:id>', methods=['POST'])
def edit_zjxxgl_save(id):  
    try:  
        #获取专家信息 
        user = User.query.filter_by(id=id).first()   
        user_information = Rcs_Expert_Information.query.filter_by(expert_id=id).first()
        user_name = request.form['user_name']   
        sex = request.form['sex']   
        card_id = request.form['card_id']   
        mobile = request.form['phone']   
        level = request.form['level']
        org = request.form['org']

        address = request.form['address']
        hy = request.form['hy']
        qy = request.form['qy']
        product = request.form['product']
        balance = request.form['balance']
        zyzc = request.form['zyzc']
        xrzw = request.form['xrzw']
        expert_level = request.form['expert_level']
        approve_role = request.form['approve_role']
        gzr = request.form['gzr']
        gzsd = request.form['gzsd']
        user.login_name=user_name
        user.real_name=user_name
        user.sex=sex
        user.card_id=card_id
        user.mobile=mobile
        user.user_type=level
        user.org_id=org

        user_information.address=address
        user_information.hy=hy
        user_information.qy=qy
        user_information.product=product
        user_information.balance=balance
        user_information.zyzc=zyzc
        user_information.xrzw=xrzw
        user_information.expert_level=expert_level
        user_information.approve_role=approve_role
        user_information.gzr=gzr
        user_information.gzsd=gzsd
      
        db.session.commit()
        flash('保存成功','success')
    except:
        # 回滚
        db.session.rollback()
        logger.exception('exception')
        # 消息闪现
        flash('保存失败','error')
    return redirect('/pgzjgl/zjxxgl')

@app.route('/pgzjgl/show_zjxxgl/<int:id>', methods=['GET'])
def show_zjxxgl(id):    
    #获取专家信息 
    user = User.query.filter_by(id=id).first()
    user_information = Rcs_Expert_Information.query.filter_by(expert_id=id).first()     
    return render_template("pgzjgl/show_zjxxgl.html",user=user,user_information=user_information)

@app.route('/pgzjgl/zjcjgl', methods=['GET'])
@login_required
def zjcjgl():        
    return render_template("pgzjgl/zjcjgl.html")

@app.route('/pgzjgl/edit_zjcjgl', methods=['GET'])
def edit_zjcjgl():        
    return render_template("pgzjgl/edit_zjcjgl.html")

@app.route('/pgzjgl/show_zjcjgl', methods=['GET'])
def show_zjcjgl():        
    return render_template("pgzjgl/show_zjcjgl.html")

@app.route('/pgzjgl/zjzxpgqxgl', methods=['GET'])
@login_required
def zjzxpgqxgl():        
    return render_template("pgzjgl/zjzxpgqxgl.html")

@app.route('/pgzjgl/edit_zjzxpgqxgl', methods=['GET'])
def edit_zjzxpgqxgl():        
    return render_template("pgzjgl/edit_zjzxpgqxgl.html")

@app.route('/pgzjgl/show_zjzxpgqxgl', methods=['GET'])
def show_zjzxpgqxgl():        
    return render_template("pgzjgl/show_zjzxpgqxgl.html")

@app.route('/pgzjgl/zjjcgl', methods=['GET'])
@login_required
def zjjcgl():        
    return render_template("pgzjgl/zjjcgl.html")

@app.route('/pgzjgl/show_zjjcgl', methods=['GET'])
def show_zjjcgl():        
    return render_template("pgzjgl/show_zjjcgl.html")

@app.route('/pgzjgl/edit_zjjcgl', methods=['GET'])
def edit_zjjcgl():        
    return render_template("pgzjgl/edit_zjjcgl.html")

@app.route('/pgzjgl/zjywlgl', methods=['GET'])
@login_required
def zjywlgl():        
    return render_template("pgzjgl/zjywlgl.html")

@app.route('/pgzjgl/show_zjywlgl', methods=['GET'])
def show_zjywlgl():        
    return render_template("pgzjgl/show_zjywlgl.html")

@app.route('/pgzjgl/zjpgzlgl', methods=['GET'])
@login_required
def zjpgzlgl():        
    return render_template("pgzjgl/zjpgzlgl.html")

@app.route('/pgzjgl/show_zjpgzlgl', methods=['GET'])
def show_zjpgzlgl():        
    return render_template("pgzjgl/show_zjpgzlgl.html")

@app.route('/pgzjgl/zjjxgl', methods=['GET'])
@login_required
def zjjxgl():        
    return render_template("pgzjgl/zjjxgl.html")

@app.route('/pgzjgl/show_zjjxgl', methods=['GET'])
def show_zjjxgl():        
    return render_template("pgzjgl/show_zjjxgl.html")

# =================================互联网数据抓取==================
@app.route('/by_bigdata',methods=['GET', 'POST'])
@login_required
def re_bigdata():
    return redirect('http://192.168.1.137:8080/jbda/home/loginTest.do?userName=test&userPwd=test')
