# coding:utf-8
import hashlib

from RemoteCreditSystem import User
from RemoteCreditSystem.models.system_usage.Rcs_Application_Info import Rcs_Application_Info
from RemoteCreditSystem.models.system_usage.Rcs_Application_Advice import Rcs_Application_Advice
from RemoteCreditSystem.models.system_usage.Rcs_Application_Score import Rcs_Application_Score
from RemoteCreditSystem.models.system_usage.Rcs_Parameter import Rcs_Parameter
from flask import request, render_template,flash,redirect
from flask.ext.login import login_user, logout_user, current_user, login_required
from RemoteCreditSystem import app
from RemoteCreditSystem import db
from RemoteCreditSystem.config import PER_PAGE

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
    
# 欢迎界面
@app.route('/login_wel', methods=['POST'])
def login_wel():
    if request.method == 'POST':
        user = User.query.filter_by(login_name=request.form['login_name'], login_password=GetStringMD5(request.form['login_password'])).first()
        if user:
            return render_template("index.html")
        else:
            flash('用户名或密码错误','error')
            return render_template("login.html")  

# welcome
@app.route('/welcome', methods=['GET'])
def welcome():        
    return render_template("welcome.html")


@app.route('/jjrwfa/zxpg', methods=['GET'])
def zxpg():        
    return render_template("jjrwfa/zxpg.html")

#进件分案页面
@app.route('/jjrwfa/jjfa/<int:page>', methods=['GET'])
def jjfa(page): 
    #获取未分类数据     
    appList = Rcs_Application_Info.query.filter_by(approve_type='1').paginate(page, per_page = PER_PAGE)
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

@app.route('/jjrwfa/rgfa/<int:userId>', methods=['GET'])
def rgfa(userId):        
    app = Rcs_Application_Info.query.filter_by(id=userId).first()  
    return render_template("jjrwfa/rgfa.html",app=app)

@app.route('/jjrwfa/xtfa', methods=['GET'])
def xtfa():        
    return render_template("jjrwfa/xtfa.html")

@app.route('/jjrwfa/show_jjfa/<int:userId>', methods=['GET'])
def show_jjfa(userId):  
    app = Rcs_Application_Info.query.filter_by(id=userId).first()   
    return render_template("jjrwfa/show_jjfa.html",app=app)

@app.route('/jjrwfa/insert_jjfa/<int:id>', methods=['GET'])
def insert_jjfa(id):  
    app = Rcs_Application_Info.query.filter_by(id=id).first()   
    app.approve_type="2"
    db.session.commit()
    flash('保存成功','success')
    return redirect("/jjrwfa/jjfa/1")

#信息导入
@app.route('/mxpg/xxdr', methods=['GET'])
def xxdr():      
    return render_template("mxpg/iframe.html")

@app.route('/mxpg/pldr', methods=['GET'])
def pldr():      
    return render_template("mxpg/pldr.html")
@app.route('/mxpg/xxlr', methods=['GET'])
def xxlr():      
    #获取未分类数据     
    appList = Rcs_Application_Info.query.filter_by(approve_type='1').all()
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

#查看评估报告
@app.route('/mxpg/show_pgbg/<int:id>', methods=['GET'])
def show_pgbg(id):    
    score = Rcs_Application_Score.query.filter_by(application_id=id).first()
    return render_template("mxpg/show_pgbg.html",score=score)

#参数管理
@app.route('/mxpg/csgl', methods=['GET'])
def csgl():  
    #添加四级联动(行业)
    list1 = db.session.execute("select concat(ABVENNAME,'_',ENNAME) as name,CNNAME as title from std_gb where (length(locate)-length(replace(locate,',','')))=2")
    list2 = db.session.execute("select concat(ABVENNAME,'_',ENNAME) as name,CNNAME as title from std_gb where (length(locate)-length(replace(locate,',','')))=3")
    list3 = db.session.execute("select concat(ABVENNAME,'_',ENNAME) as name,CNNAME as title from std_gb where (length(locate)-length(replace(locate,',','')))=4")
    list4 = db.session.execute("select concat(ABVENNAME,'_',ENNAME) as name,CNNAME as title from std_gb where (length(locate)-length(replace(locate,',','')))=5")
    #区域三级联动
    list11 = db.session.execute("select concat(parent_code,'_',type_code) as name,type_name as title from INDIV_BRT_PLACE where levels = 1 order by name")
    list22 = db.session.execute("select concat(parent_code,'_',type_code) as name,type_name as title from INDIV_BRT_PLACE where levels = 2 order by name")
    list33 = db.session.execute("select concat(parent_code,'_',type_code) as name,type_name as title from INDIV_BRT_PLACE where levels = 3 order by name")
    return render_template("mxpg/csgl.html",list1=list1,list2=list2,list3=list3,list4=list4,list11=list11,list22=list22,list33=list33)
#参数配置--进入iframe
@app.route('/mxpg/iframe_cspz', methods=['GET'])
def iframe_cspz():    
    return render_template("mxpg/iframe_cspz.html")

#参数配置--道德品质
@app.route('/mxpg/cspz_ddpz', methods=['GET'])
def cspz_ddpz():
    ddpz = Rcs_Parameter.query.filter_by(parameter_name="ddpz").first()
    result=ddpz.parameter_value
    return render_template("mxpg/cspz_ddpz.html",result=result)

#参数配置--道德品质--保存
@app.route('/mxpg/cspz_ddpz_save/<score>', methods=['GET'])
def cspz_ddpz_save(score):
    Rcs_Parameter("ddpz",score).add()
    db.session.commit()
    return redirect("/mxpg/cspz_ddpz")

#参数配置--经营状况
@app.route('/mxpg/cspz_jyzk', methods=['GET'])
def cspz_jyzk():    
    return render_template("mxpg/cspz_jyzk.html")

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

#还款能力页面
@app.route('/khzldy/khzl_hknl/<int:id>', methods=['GET'])
def khzl_hknl(id):        
    return render_template("customer/iframe.html",id=id)

#资产负债
@app.route('/khzldy/zcfzzk/<int:id>', methods=['GET'])
def zcfzzk(id):        
    return render_template("customer/zcfzzk.html")
#利润表
@app.route('/khzldy/lrb/<int:id>', methods=['GET'])
def lrb(id):        
    return render_template("customer/lrb.html")

#现金流量
@app.route('/khzldy/xjll/<int:id>', methods=['GET'])
def xjll(id):        
    return render_template("customer/xjll.html")

#交叉检验
@app.route('/khzldy/jcjy/<int:id>', methods=['GET'])
def jcjy(id):        
    return render_template("customer/jcjy.html")

#经营状况
@app.route('/khzldy/khzl_jyzk/<int:id>', methods=['GET'])
def khzl_jyzk(id):        
    return render_template("customer/jyzk.html")

#生活状态
@app.route('/khzldy/khzl_shzk/<int:id>', methods=['GET'])
def khzl_shzk(id):        
    return render_template("customer/shzt.html")

#道德品质
@app.route('/khzldy/khzl_ddpz/<int:id>', methods=['GET'])
def khzl_ddpz(id): 
    ddpz = Rcs_Parameter.query.filter_by(parameter_name="ddpz").first()
    result=ddpz.parameter_value
    return render_template("customer/ddpz.html",result=result,id=id)

#道德品质保存
@app.route('/khzldy/khzl_ddpz_save/<int:id>', methods=['POST'])
def khzl_ddpz_save(id):     
    total = request.form['score_result'] 
    score = Rcs_Application_Score.query.filter_by(application_id=id).first()
    if score:
        score.ddpz_score=total
    else:
        Rcs_Application_Score(id,total,"","","").add()
    db.session.commit()
    return redirect("/khzldy/khzl_ddpz/"+str(id))

@app.route('/zjzxpggl/jjrw', methods=['GET'])
def jjrw(): 
    #获取进件任务数据
    appList = Rcs_Application_Info.query.filter_by(approve_type='2').all()
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
    appList = Rcs_Application_Info.query.filter_by(approve_type='3').all()   
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

    Rcs_Application_Advice(id,request.form['approve_idea'],request.form['approve_result'],request.form['approve_ed'],'').add()

    db.session.commit()    
    return redirect("/zjzxpggl/yjsrw")

@app.route('/zjzxpggl/yjjrw', methods=['GET'])
def yjjrw():    
    appList = Rcs_Application_Info.query.filter_by(approve_type='4').all()       
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
@app.route('/zxpgjl/pgjl', methods=['GET'])
def pgjl():   
    appList = Rcs_Application_Info.query.filter_by(approve_type='5').all()     
    return render_template("zxpgjl/pgjl.html",appList=appList)

@app.route('/zxpgjl/pgjl_info/<int:id>', methods=['GET'])
def pgjl_info(id):        
    app = Rcs_Application_Info.query.filter_by(id=id).first()
    advice = Rcs_Application_Advice.query.filter_by(application_id=id).first()
    return render_template("zxpgjl/pgjl_info.html",app=app,advice=advice)

@app.route('/zxpggzwh/pggzwh', methods=['GET'])
def pggzwh():        
    return render_template("zxpggzwh/pggzwh.html")

#专家信息管理
@app.route('/pgzjgl/zjxxgl', methods=['GET'])
def zjxxgl():
    #获取专家信息 
    user = User.query.filter_by(user_type='1').all()          
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
    User(user_name,GetStringMD5('111111'),user_name,sex,phone,1,'',card_id,zjzz,remark1,zjqx,remark2,bhxx,remark3,'1',role).add()  
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
