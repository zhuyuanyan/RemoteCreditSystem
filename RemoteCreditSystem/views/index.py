# coding:utf-8
import hashlib

from RemoteCreditSystem import User
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
from flask import request, render_template,flash,redirect
from flask.ext.login import login_user, logout_user, current_user, login_required
from RemoteCreditSystem import app
from RemoteCreditSystem import db
from RemoteCreditSystem.config import Application_Type_Create,Application_Type_Approve,Application_Type_Finish
from RemoteCreditSystem.config import logger
from RemoteCreditSystem.config import PER_PAGE

from RemoteCreditSystem.tools.SimpleCache import SimpleCache

from RemoteCreditSystem.models import Rcs_Application_Log,Rcs_Application_Absent


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
    
# 欢迎界面
@app.route('/login_wel', methods=['POST','GET'])
def login_wel():
    if request.method == 'POST':
        user = User.query.filter_by(login_name=request.form['login_name'], login_password=GetStringMD5(request.form['login_password'])).first()
        simplecache = SimpleCache.getInstance()
        if user:
            login_user(user)
            role_id = UserRole.query.filter_by(user_id=current_user.id).first().role_id
            rcs_access_right = Rcs_Access_Right.query.filter_by(role_id=role_id).order_by("id").all()
            tree = []
            if(user.login_name == 'admin'):
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
            
            return render_template("index.html",loginName=request.form['login_name'],tree=tree)
        else:
            flash('用户名或密码错误','error')
            return render_template("login.html")  
    else:
        return render_template("login.html")

# welcome
@app.route('/welcome', methods=['GET'])
def welcome():        
    return render_template("welcome.html")

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
def zxpg():        
    return render_template("jjrwfa/zxpg.html")

#进件分案页面
@app.route('/jjrwfa/jjfa/<int:page>', methods=['GET','POST'])
def jjfa(page):
    sql=" approve_type="+str(Application_Type_Create)
    if current_user.user_type:
        if str(current_user.user_type)!='2':
            sql+=" and create_user="+str(current_user.id)
    else:
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
    return render_template("jjrwfa/jjfa.html",appList=appList,current_user=current_user)

@app.route('/jjrwfa/jjrwfaxx', methods=['GET'])
def jjrwfaxx():        
    return render_template("jjrwfa/jjrwfaxx.html")

@app.route('/jjrwfa/zxpgmsgzwh', methods=['GET'])
def zxpgmsgzwh():        
    return render_template("jjrwfa/zxpgmsgzwh.html")

@app.route('/jjrwfa/fagzwh', methods=['GET'])
def fagzwh():        
    return render_template("jjrwfa/fagzwh.html")

@app.route('/jjrwfa/zxpgzjhsgzwh', methods=['GET'])
def zxpgzjhsgzwh():        
    return render_template("jjrwfa/zxpgzjhsgzwh.html")

#进入新增进件页面
@app.route('/jjrwfa/new_jjfa', methods=['GET'])
def new_jjfa():        
    return render_template("jjrwfa/new_jjfa.html")

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
        Rcs_Application_Info(index_id,name,card_id,product_id,approve_limit,org_id,place_all_name,place_all,industry_id,district_id,manager_id,sh_user,sp_user,approve_type,model_type).add()
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

@app.route('/jjrwfa/insert_jjfa/<int:id>/<expertId>', methods=['GET'])
def insert_jjfa(id,expertId):  
    app = Rcs_Application_Info.query.filter_by(id=id).first()   
    app.approve_type=Application_Type_Approve
    ids = expertId.split(",")
    for obj in ids:
        Rcs_Application_Expert(id,int(obj)).add()
    db.session.commit()
    flash('保存成功','success')
    return redirect("/jjrwfa/jjfa/1")


@app.route('/mxpg/pldr', methods=['GET'])
def pldr():      
    return render_template("mxpg/pldr.html")
@app.route('/mxpg/xxlr/<int:page>', methods=['GET','POST'])
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
@app.route('/mxpg/sxpg', methods=['GET'])
def sxpg(): 
    #获取未分类数据     
    appList = Rcs_Application_Info.query.filter_by(approve_type='1').all()     
    return render_template("mxpg/sxpg.html",appList=appList)

#评估报告
@app.route('/mxpg/pgbg', methods=['GET'])
def pgbg():      
    #获取未分类数据     
    appList = Rcs_Application_Info.query.filter_by(approve_type='1').all() 
    return render_template("mxpg/pgbg.html",appList=appList)


#参数管理
@app.route('/mxpg/csgl', methods=['GET'])
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
    return render_template("khzldy/khzl.html",appList=appList)

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
def jjrw(): 
    #获取进件任务数据  
    appList = Rcs_Application_Info.query.filter("approve_type='2' and id in (select application_id from rcs_application_expert where expert_id="+str(current_user.id)+")").all()
    return render_template("zjzxpggl/jjrw.html",appList=appList)

# @app.route('/zjzxpggl/jjrw_accept/<int:id>', methods=['GET'])
# def jjrw_accept(id): 
#     app = Rcs_Application_Info.query.filter_by(id=id).first()
#     app.approve_type="3"
#     db.session.commit()
#     return redirect("/zjzxpggl/jjrw")
# @app.route('/zjzxpggl/jjrw_refuse/<int:id>', methods=['GET'])
# def jjrw_refuse(id): 
#     app = Rcs_Application_Info.query.filter_by(approve_type='2').first()
#     app.approve_type="4"
#     db.session.commit()
#     return redirect("/zjzxpggl/jjrw")
@app.route('/zjzxpggl/yjsrw/<int:page>', methods=['GET','POST'])
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
    return render_template("zjzxpggl/yjsrw.html",appList=appList)

# @app.route('/zjzxpggl/yjsrw_refuse/<int:id>', methods=['GET'])
# def yjsrw_refuse(id):     
#     app = Rcs_Application_Info.query.filter_by(id=id).first()   
#     app.approve_type="4"
#     db.session.commit()
#     return redirect("/zjzxpggl/yjsrw")


# @app.route('/zjzxpggl/yjjrw', methods=['GET'])
# def yjjrw():    
#     appList = Rcs_Application_Info.query.filter("approve_type='4' and id in (select application_id from rcs_application_expert where expert_id="+str(current_user.id)+")").all()     
#     return render_template("zjzxpggl/yjjrw.html",appList=appList)
# @app.route('/zjzxpggl/yjjrw_accept/<int:id>', methods=['GET'])
# def yjjrw_accept(id):    
#     app = Rcs_Application_Info.query.filter_by(id=id).first()  
#     app.approve_type="3"
#     db.session.commit()     
#     return redirect("/zjzxpggl/yjjrw")
# #拒绝原因页面
# @app.route('/zjzxpggl/yjjrw_jjyy/<int:id>', methods=['GET'])
# def yjjrw_jjyy(id):  
#     app = Rcs_Application_Info.query.filter_by(id=id).first()
#     advice = Rcs_Application_Advice.query.filter_by(application_id=id).first()     
#     return render_template("zjzxpggl/yjjrw_jjyy.html",app=app,advice=advice)
# #拒绝原因页面提交
# @app.route('/zjzxpggl/yjjrw_jjyy_save/<int:id>', methods=['POST'])
# def yjjrw_jjyy_save(id):  
#     app = Rcs_Application_Info.query.filter_by(id=id).first()  
#     app.approve_type="4"

#     db.session.commit()       
#     return redirect("/zjzxpggl/yjjrw")

#评估结论查看
@app.route('/zxpgjl/pgjl/<int:page>', methods=['GET'])
def pgjl(page):   
    appList = Rcs_Application_Info.query.filter("approve_type in (2,3)").paginate(page, per_page = PER_PAGE) 
    return render_template("zxpgjl/pgjl.html",appList=appList)

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
        advice = Rcs_Application_Advice.query.filter_by(application_id=id,user_id=current_user.id).first()
        if advice:
            advice.approve_result = last_advice
            advice.approve_ed = last_approve
        else:
            Rcs_Application_Advice(id,"",last_advice,last_approve,"2").add()
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



@app.route('/zxpggzwh/pggzwh', methods=['GET'])
def pggzwh():        
    return render_template("zxpggzwh/pggzwh.html")

#专家信息管理
@app.route('/pgzjgl/zjxxgl', methods=['GET'])
def zjxxgl():
    #获取专家信息 
    user = User.query.filter("user_type='1' or user_type='2'").all()          
    return render_template("pgzjgl/zjxxgl.html",user=user)
#新增
@app.route('/pgzjgl/new_zjxxgl', methods=['GET'])
def new_zjxxgl():  
    return render_template("pgzjgl/new_zjxxgl.html")

#新增保存
@app.route('/pgzjgl/new_zjxxgl_save', methods=['POST'])
def new_zjxxgl_save():    
    user_name = request.form['user_name']   
    sex = request.form['sex']   
    card_id = request.form['card_id']   
    phone = request.form['phone']   
    zjzz = request.form['zjzz']    
    remark1 = request.form['remark1']   
    zjqx = request.form['zjqx']   
    remark2 = request.form['remark2']   
    bhxx = request.form['bhxx']  
    remark3 = request.form['remark3']
    role = request.form['role'] 
    level = request.form['level']
    User(user_name,GetStringMD5('111111'),user_name,sex,phone,1,'',card_id,zjzz,remark1,zjqx,remark2,bhxx,remark3,level,role).add()  
    db.session.commit()
    return redirect('/pgzjgl/zjxxgl')

#修改页面
@app.route('/pgzjgl/edit_zjxxgl/<int:id>', methods=['GET'])
def edit_zjxxgl(id):    
    #获取专家信息 
    user = User.query.filter_by(id=id).first()   
    return render_template("pgzjgl/edit_zjxxgl.html",user=user)
#修改提交
@app.route('/pgzjgl/edit_zjxxgl_save/<int:id>', methods=['POST'])
def edit_zjxxgl_save(id):    
    #获取专家信息 
    user = User.query.filter_by(id=id).first()   
    user_name = request.form['user_name']   
    sex = request.form['sex']   
    card_id = request.form['card_id']   
    mobile = request.form['phone']   
    zjzz = request.form['zjzz']    
    remark1 = request.form['remark1']   
    zjqx = request.form['zjqx']   
    remark2 = request.form['remark2']   
    bhxx = request.form['bhxx']  
    remark3 = request.form['remark3']
    role = request.form['role']
    user.login_name=user_name
    user.real_name=user_name
    user.sex=sex
    user.card_id=card_id
    user.mobile=mobile
    user.zjzz=zjzz
    user.remark1=remark1
    user.zjqx=zjqx
    user.remark2=remark2
    user.bhxx=bhxx
    user.remark3=remark3
    user.role=role
    db.session.commit()
    return redirect('/pgzjgl/zjxxgl')

@app.route('/pgzjgl/show_zjxxgl/<int:id>', methods=['GET'])
def show_zjxxgl(id):    
    #获取专家信息 
    user = User.query.filter_by(id=id).first()      
    return render_template("pgzjgl/show_zjxxgl.html",user=user)

@app.route('/pgzjgl/zjcjgl', methods=['GET'])
def zjcjgl():        
    return render_template("pgzjgl/zjcjgl.html")

@app.route('/pgzjgl/edit_zjcjgl', methods=['GET'])
def edit_zjcjgl():        
    return render_template("pgzjgl/edit_zjcjgl.html")

@app.route('/pgzjgl/show_zjcjgl', methods=['GET'])
def show_zjcjgl():        
    return render_template("pgzjgl/show_zjcjgl.html")

@app.route('/pgzjgl/zjzxpgqxgl', methods=['GET'])
def zjzxpgqxgl():        
    return render_template("pgzjgl/zjzxpgqxgl.html")

@app.route('/pgzjgl/edit_zjzxpgqxgl', methods=['GET'])
def edit_zjzxpgqxgl():        
    return render_template("pgzjgl/edit_zjzxpgqxgl.html")

@app.route('/pgzjgl/show_zjzxpgqxgl', methods=['GET'])
def show_zjzxpgqxgl():        
    return render_template("pgzjgl/show_zjzxpgqxgl.html")

@app.route('/pgzjgl/zjjcgl', methods=['GET'])
def zjjcgl():        
    return render_template("pgzjgl/zjjcgl.html")

@app.route('/pgzjgl/show_zjjcgl', methods=['GET'])
def show_zjjcgl():        
    return render_template("pgzjgl/show_zjjcgl.html")

@app.route('/pgzjgl/edit_zjjcgl', methods=['GET'])
def edit_zjjcgl():        
    return render_template("pgzjgl/edit_zjjcgl.html")

@app.route('/pgzjgl/zjywlgl', methods=['GET'])
def zjywlgl():        
    return render_template("pgzjgl/zjywlgl.html")

@app.route('/pgzjgl/show_zjywlgl', methods=['GET'])
def show_zjywlgl():        
    return render_template("pgzjgl/show_zjywlgl.html")

@app.route('/pgzjgl/zjpgzlgl', methods=['GET'])
def zjpgzlgl():        
    return render_template("pgzjgl/zjpgzlgl.html")

@app.route('/pgzjgl/show_zjpgzlgl', methods=['GET'])
def show_zjpgzlgl():        
    return render_template("pgzjgl/show_zjpgzlgl.html")

@app.route('/pgzjgl/zjjxgl', methods=['GET'])
def zjjxgl():        
    return render_template("pgzjgl/zjjxgl.html")

@app.route('/pgzjgl/show_zjjxgl', methods=['GET'])
def show_zjjxgl():        
    return render_template("pgzjgl/show_zjjxgl.html")

# =================================互联网数据抓取==================
@app.route('/by_bigdata',methods=['GET', 'POST'])
def re_bigdata():
    return redirect('http://192.168.1.137:8080/jbda/home/loginTest.do?userName=test&userPwd=test')
