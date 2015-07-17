# coding:utf-8
import hashlib

from RemoteCreditSystem import User
from RemoteCreditSystem.models import UserRole,Rcs_Access_Right
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
from RemoteCreditSystem.config import logger
from RemoteCreditSystem.config import PER_PAGE

from RemoteCreditSystem.tools.SimpleCache import SimpleCache

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
@app.route('/jjrwfa/jjfa/<int:page>', methods=['GET'])
def jjfa(page): 
    #获取未分类数据     
    appList = Rcs_Application_Info.query.filter_by(approve_type='1',create_user=current_user.id).paginate(page, per_page = PER_PAGE)
    return render_template("jjrwfa/jjfa.html",appList=appList)

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
    print "----"
    name = request.form['name']
    card_id = request.form['card_id']
    db.engine.execute("insert into rcs_application_info(customer_name,card_id,approve_type,create_user) values('"+name+"','"+card_id+"','1',"+str(current_user.id)+")")

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
    app.approve_type="2"
    ids = expertId.split(",")
    for obj in ids:
        Rcs_Application_Expert(id,int(obj)).add()
    db.session.commit()
    flash('保存成功','success')
    return redirect("/jjrwfa/jjfa/1")


@app.route('/mxpg/pldr', methods=['GET'])
def pldr():      
    return render_template("mxpg/pldr.html")
@app.route('/mxpg/xxlr', methods=['GET'])
def xxlr():      
    #获取未分类数据     
    appList = Rcs_Application_Info.query.filter_by(create_user=current_user.id).all()
    for obj in appList:
        if not obj.model_type:
            obj.model_type="0"
    return render_template("mxpg/xxlr.html",appList=appList)

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
@app.route('/khzldy/khzl', methods=['GET'])
def khzl():      
    #获取未分类数据     
    appList = Rcs_Application_Info.query.all()
    return render_template("khzldy/khzl.html",appList=appList)
#客户资料
@app.route('/khzldy/khzl_info', methods=['GET'])
def khzl_info():        
    return render_template("customer/jbzl.html")

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

#还款能力保存
@app.route('/khzldy/khzl_hknl_save/<int:id>', methods=['POST'])
def khzl_hknl_save(id):     
    total = request.form['score_result'] 
    remark = request.form['score_remark'] 
    score = Rcs_Application_Score.query.filter_by(application_id=id).first()
    if score:
        score.hknl_score=total
    else:
        Rcs_Application_Score(id,"",total,"","",remark,"").add()
    db.session.commit()
    return redirect("/khzldy/khzl_hk/"+str(id))

#资产负债
@app.route('/khzldy/zcfzzk/<int:id>', methods=['GET'])
def zcfzzk(id):   
    zcfzbData = Rcs_Application_Zcfzb.query.filter_by(application_id=id).first()
    return render_template("customer/zcfzzk.html",id=id,data=zcfzbData)
#资产负债---保存
@app.route('/khzldy/zcfzzk_save/<int:id>', methods=['POST'])
def zcfzzk_save(id):   
    zcfzl = request.form['zcfzl']   
    ldbl = request.form['ldbl']   
    sdbl = request.form['sdbl']
    #交叉检验所需年营业额
    yye3 = request.form['yye3']
    #交叉检验所需存货检验
    yye10 = request.form['yye10']
    yye11 = request.form['yye11']
    #存货总额
    value_1 = request.form['value_19']
    #总资产
    value_2 = request.form['value_29']
    #流动资产总和
    value_3 = request.form['value_22']
    #实际权益
    value_37 = request.form['value_37']
    result = Rcs_Application_Result.query.filter_by(application_id=id).first()
    if result:
        result.zcfzl=zcfzl
        result.ldbl=ldbl
        result.sdbl=sdbl
        result.value_1=value_1
        result.value_2=value_2
        result.value_3=value_3
    else:
        Rcs_Application_Result(id,zcfzl,ldbl,sdbl,value_1,value_2,value_3,"","","").add()
    #交叉检验
    result1 = Rcs_Application_Jcjy.query.filter_by(application_id=id).first()
    if result1:
        result1.value3=yye3
        result1.value10=yye10
        result1.value11=yye11
        result1.value15=value_37
    else:
        Rcs_Application_Jcjy(id,"","",yye3,"","","","","","",yye10,yye11,"","","",value_37,"","","").add()
    
    #资产负债表页面form数据保存
    #form json值
    dataTotal = request.form['dataTotal']
    zcfzbData = Rcs_Application_Zcfzb.query.filter_by(application_id=id).first()
    if zcfzbData:
        zcfzbData.value_1=dataTotal
    else:
        Rcs_Application_Zcfzb(id,dataTotal,'').add()

    info = Rcs_Application_Info.query.filter_by(id=id).first()
    if info:
        #设置为传统模型
        info.model_type=1
    db.session.commit()
    return redirect("/khzldy/zcfzzk/"+str(id))

#利润表
@app.route('/khzldy/lrb/<int:id>', methods=['GET'])
def lrb(id):        
    appResult = Rcs_Application_Result.query.filter_by(application_id=id).first()
    if not appResult:
        appResult = Rcs_Application_Result(id,"","","","","","","","","").add()
    db.session.commit()
    appResult = Rcs_Application_Result.query.filter_by(application_id=id).first()
    #页面数据
    data = Rcs_Application_Lrb.query.filter_by(application_id=id).first()
    return render_template("customer/lrb.html",appResult=appResult,id=id,data=data)

#利润表--保存
@app.route('/khzldy/lrb_save/<int:id>', methods=['POST'])
def lrb_save(id):   
    #存货周转率    
    chzzl = request.form['chzzl']
    if not chzzl:
        chzzl=0
    #总资产周转率
    zzczzl = request.form['zzczzl']
    if not zzczzl:
        zzczzl=0
    #净利润
    value = request.form['value_13']
    value_1 = request.form['yye1']
    value_2 = request.form['yye2']
    value_4 = request.form['yye4']
    value_6 = request.form['yye6']
    value_7 = request.form['yye7']
    value_8 = request.form['yye8']
    value_9 = request.form['yye9']
    value_13 = request.form['yye13']
    value_17 = request.form['yye17']
    value_18 = request.form['yye18']
    #还款能力结果表
    appResult = Rcs_Application_Result.query.filter_by(application_id=id).first()
    if not appResult:
        Rcs_Application_Result(id,"","","","","","",chzzl,zzczzl,value_13).add()
    else:
        appResult.chzzl=chzzl
        appResult.zzczzl=zzczzl
        appResult.value_13=value

    #交叉检验表
    jcjy = Rcs_Application_Jcjy.query.filter_by(application_id=id).first()
    if jcjy:
        jcjy.value1=value_1
        jcjy.value2=value_2
        jcjy.value4=value_4
        jcjy.value6=value_6
        jcjy.value7=value_7
        jcjy.value8=value_8
        jcjy.value9=value_9
        jcjy.value13=value_13
        jcjy.value17=value_17
        jcjy.value18=value_18
    else:
        Rcs_Application_Jcjy(id,value_1,value_2,"",value_4,"",value_6,value_7,value_8,value_9,"","","",value_13,"","","",value_17,value_18).add()

    #利润表页面form数据保存
    #form json值
    dataTotal = request.form['dataTotal']
    dataTotalSelect = request.form['dataTotalSelect']
    lrbData = Rcs_Application_Lrb.query.filter_by(application_id=id).first()
    if lrbData:
        lrbData.value_1=dataTotal
        lrbData.value_2=dataTotalSelect
    else:
        Rcs_Application_Lrb(id,dataTotal,dataTotalSelect).add()

    #保存还款能力分值(月可支)
    score = Rcs_Application_Score.query.filter_by(application_id=id).first()
    if score:
        score.hknl_score = float('%.2f'% float(value_17))
        if score.ddpz_score and score.hknl_score and score.jyzk_score and score.shzk_score:
            totalScore = float(score.ddpz_score)*float(score.hknl_score)*float(score.jyzk_score)*float(score.shzk_score)
            score.total_approve = float('%.2f'% totalScore) 
    else:
        Rcs_Application_Score(id,"",float('%.2f'% float(value_17)),"","","","").add()

    info = Rcs_Application_Info.query.filter_by(id=id).first()
    if info:
        #设置为传统模型
        info.model_type=1
    db.session.commit()
    return redirect("khzldy/lrb/"+str(id))

#现金流量
@app.route('/khzldy/xjll/<int:id>', methods=['GET'])
def xjll(id):    
    result = Rcs_Application_Xjll.query.filter_by(application_id=id).first()
    return render_template("customer/xjll.html",id=id,result=result)

#现金流量--保存
@app.route('/khzldy/xjll_save/<int:id>', methods=['POST'])
def xjll_save(id):  
    Rcs_Application_Xjll.query.filter_by(application_id=id).delete()
    qcxj = request.form['qcxj']
    jyxxjlr = request.form['jyxxjlr']   
    jyxxjlc = request.form['jyxxjlc']   
    jyxjjll = request.form['jyxjjll']   
    tzxjlr = request.form['tzxjlr']   
    tzxjlc = request.form['tzxjlc']   
    tzxjjll = request.form['tzxjjll']   
    rzxjlr = request.form['rzxjlr']   
    rzxjlc = request.form['rzxjlc']   
    rzxjjll = request.form['rzxjjll']   
    qmxj = request.form['qmxj']   
    qcqysd = request.form['qcqysd']   
    qcqyhj = request.form['qcqyhj']   
    fxqjsr = request.form['fxqjsr']   
    qtsr = request.form['qtsr']   
    sz = request.form['sz']   
    dxzchj = request.form['dxzchj']   
    zj = request.form['zj']   
    bz = request.form['bz']   
    bwzc = request.form['bwzc']   
    Rcs_Application_Xjll(id,qcxj,jyxxjlr,jyxxjlc,jyxjjll,tzxjlr,tzxjlc,tzxjjll,rzxjlr,rzxjlc,rzxjjll,qmxj,qcqysd,qcqyhj,fxqjsr,qtsr,sz,dxzchj,zj,bz,bwzc).add()
    db.session.commit()
    return redirect("/khzldy/xjll/"+str(id))

#交叉检验
@app.route('/khzldy/jcjy/<int:id>', methods=['GET'])
def jcjy(id):        
    return render_template("customer/jcjy.html")

#经营状况
@app.route('/khzldy/khzl_jyzk/<int:id>', methods=['GET'])
def khzl_jyzk(id):
    jyzk = Rcs_Parameter.query.filter_by(parameter_name="jyzk").first()
    result = ""
    if jyzk :
        result=jyzk.parameter_value
    #页面数据
    data = Rcs_Application_Jyzk.query.filter_by(application_id=id).first()
    return render_template("customer/jyzk.html",result=result,id=id,data=data)
#经营状况保存
@app.route('/khzldy/khzl_jyzk_save/<int:id>', methods=['POST'])
def khzl_jyzk_save(id):  
    total = request.form['score_result'] 
    remark = request.form['score_remark'] 
    score = Rcs_Application_Score.query.filter_by(application_id=id).first()
    if score:
        score.jyzk_score=total
    else:
        Rcs_Application_Score(id,"","",total,"",remark,"").add()

    #经营状况页面form数据保存
    #form json值
    dataTotal = request.form['dataTotal']
    dataTotalSelect = request.form['dataTotalSelect']
    lrbData = Rcs_Application_Jyzk.query.filter_by(application_id=id).first()
    if lrbData:
        lrbData.value_1=dataTotal
        lrbData.value_2=dataTotalSelect
    else:
        Rcs_Application_Jyzk(id,dataTotal,dataTotalSelect).add()

    db.session.commit()
    return redirect("/khzldy/khzl_jyzk/"+str(id))

#生活状态
@app.route('/khzldy/khzl_shzk/<int:id>', methods=['GET'])
def khzl_shzk(id):     
    shzt = Rcs_Parameter.query.filter_by(parameter_name="shzt").first()
    result=shzt.parameter_value   
    #页面数据
    data = Rcs_Application_Shzk.query.filter_by(application_id=id).first()
    return render_template("customer/shzt.html",result=result,id=id,data=data)

#生活状态保存
@app.route('/khzldy/khzl_shzk_save/<int:id>', methods=['POST'])
def khzl_shzk_save(id):  
    total = request.form['score_result'] 
    remark = request.form['score_remark'] 
    score = Rcs_Application_Score.query.filter_by(application_id=id).first()
    if score:
        score.shzk_score=total
    else:
        Rcs_Application_Score(id,"","","",total,remark,"").add()

        #道德品质页面form数据保存
    #form json值
    dataTotal = request.form['dataTotal']
    dataTotalSelect = request.form['dataTotalSelect']
    dataTotalRadio = request.form['dataTotalRadio']
    shzkData = Rcs_Application_Shzk.query.filter_by(application_id=id).first()
    if shzkData:
        shzkData.value_1=dataTotal
        shzkData.value_2=dataTotalSelect
        shzkData.value_3=dataTotalRadio
    else:
        Rcs_Application_Shzk(id,dataTotal,dataTotalSelect,dataTotalRadio).add()

    db.session.commit()
    return redirect("/khzldy/khzl_shzk/"+str(id))

#道德品质
@app.route('/khzldy/khzl_ddpz/<int:id>', methods=['GET'])
def khzl_ddpz(id): 
    ddpz = Rcs_Parameter.query.filter_by(parameter_name="ddpz").first()
    result=ddpz.parameter_value
    #页面数据
    data = Rcs_Application_Ddpz.query.filter_by(application_id=id).first()
    return render_template("customer/ddpz.html",result=result,id=id,data=data)

#道德品质保存
@app.route('/khzldy/khzl_ddpz_save/<int:id>', methods=['POST'])
def khzl_ddpz_save(id):     
    total = request.form['score_result'] 
    remark = request.form['score_remark'] 
    score = Rcs_Application_Score.query.filter_by(application_id=id).first()
    if score:
        score.ddpz_score=total
    else:
        Rcs_Application_Score(id,total,"","","",remark,"").add()

    #道德品质页面form数据保存
    #form json值
    dataTotal = request.form['dataTotal']
    dataTotalSelect = request.form['dataTotalSelect']
    ddpzData = Rcs_Application_Ddpz.query.filter_by(application_id=id).first()
    if ddpzData:
        ddpzData.value_1=dataTotal
        ddpzData.value_2=dataTotalSelect
    else:
        Rcs_Application_Ddpz(id,dataTotal,dataTotalSelect).add()
    db.session.commit()
    return redirect("/khzldy/khzl_ddpz/"+str(id))

@app.route('/zjzxpggl/jjrw', methods=['GET'])
def jjrw(): 
    #获取进件任务数据  
    appList = Rcs_Application_Info.query.filter("approve_type='2' and id in (select application_id from rcs_application_expert where expert_id="+str(current_user.id)+")").all()
    return render_template("zjzxpggl/jjrw.html",appList=appList)

@app.route('/zjzxpggl/jjrw_accept/<int:id>', methods=['GET'])
def jjrw_accept(id): 
    app = Rcs_Application_Info.query.filter_by(id=id).first()
    app.approve_type="3"
    db.session.commit()
    return redirect("/zjzxpggl/jjrw")
@app.route('/zjzxpggl/jjrw_refuse/<int:id>', methods=['GET'])
def jjrw_refuse(id): 
    app = Rcs_Application_Info.query.filter_by(approve_type='2').first()
    app.approve_type="4"
    db.session.commit()
    return redirect("/zjzxpggl/jjrw")
@app.route('/zjzxpggl/yjsrw', methods=['GET'])
def yjsrw():     
    appList = Rcs_Application_Info.query.filter("approve_type='3' and id in (select application_id from rcs_application_expert where expert_id="+str(current_user.id)+")").all()  
    return render_template("zjzxpggl/yjsrw.html",appList=appList)

@app.route('/zjzxpggl/yjsrw_refuse/<int:id>', methods=['GET'])
def yjsrw_refuse(id):     
    app = Rcs_Application_Info.query.filter_by(id=id).first()   
    app.approve_type="4"
    db.session.commit()
    return redirect("/zjzxpggl/yjsrw")

# 开始评估
@app.route('/zjzxpggl/yjsrw_kspg/<int:id>', methods=['GET'])
def yjsrw_kspg(id):    
    app = Rcs_Application_Info.query.filter_by(id=id).first()      
    return render_template("zjzxpggl/yjsrw_kspg.html",app=app)
#评估提交
@app.route('/zjzxpggl/yjsrw_save/<int:id>', methods=['POST'])
def yjsrw_save(id):    
    app = Rcs_Application_Info.query.filter_by(id=id).first()  
    app.approve_type="5"
    #普通专家
    advice_type=1
    Rcs_Application_Advice(id,request.form['approve_idea'],request.form['approve_result'],request.form['approve_ed'],advice_type).add()

    db.session.commit()    
    return redirect("/zjzxpggl/yjsrw")

@app.route('/zjzxpggl/yjjrw', methods=['GET'])
def yjjrw():    
    appList = Rcs_Application_Info.query.filter("approve_type='4' and id in (select application_id from rcs_application_expert where expert_id="+str(current_user.id)+")").all()     
    return render_template("zjzxpggl/yjjrw.html",appList=appList)
@app.route('/zjzxpggl/yjjrw_accept/<int:id>', methods=['GET'])
def yjjrw_accept(id):    
    app = Rcs_Application_Info.query.filter_by(id=id).first()  
    app.approve_type="3"
    db.session.commit()     
    return redirect("/zjzxpggl/yjjrw")
#拒绝原因页面
@app.route('/zjzxpggl/yjjrw_jjyy/<int:id>', methods=['GET'])
def yjjrw_jjyy(id):  
    app = Rcs_Application_Info.query.filter_by(id=id).first()
    advice = Rcs_Application_Advice.query.filter_by(application_id=id).first()     
    return render_template("zjzxpggl/yjjrw_jjyy.html",app=app,advice=advice)
#拒绝原因页面提交
@app.route('/zjzxpggl/yjjrw_jjyy_save/<int:id>', methods=['POST'])
def yjjrw_jjyy_save(id):  
    app = Rcs_Application_Info.query.filter_by(id=id).first()  
    app.approve_type="4"

    db.session.commit()       
    return redirect("/zjzxpggl/yjjrw")

#评估结论查看
@app.route('/zxpgjl/pgjl/<int:page>', methods=['GET'])
def pgjl(page):   
    appList = Rcs_Application_Info.query.filter("approve_type='3'").paginate(page, per_page = PER_PAGE) 
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

@app.route('/zxpgjl/save_pgjl_info/<int:id>', methods=['POST'])
def save_pgjl_info(id):
    try:
        last_advice = request.form['last_advice']
        last_approve = request.form['last_approve']
        advice = Rcs_Application_Advice.query.filter_by(application_id=id,user_id=current_user.id).first()
        if advice:
            advice.approve_result = last_advice
            advice.approve_ed = last_approve
        else:
            Rcs_Application_Advice(id,"",last_advice,last_approve,"2").add()
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
