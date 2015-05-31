# coding:utf-8

from flask import request, render_template,flash

from RemoteCreditSystem import app
from RemoteCreditSystem.models.system_usage import User
import hashlib

#get md5 of a input string
def GetStringMD5(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()
	
# 登陆
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(login_name=request.form['login_name'], login_password=GetStringMD5(request.form['login_password'])).first()
        if user:
            render_template("welcom.html")
        else:
            flash('用户名或密码错误','error')
            return render_template("login.html")
    else:
        return render_template("login.html")
    
# 欢迎界面
@app.route('/login_wel', methods=['POST'])
def login_wel():        
    return render_template("index.html")

# welcome
@app.route('/welcome', methods=['GET'])
def welcome():        
    return render_template("welcome.html")


@app.route('/jjrwfa/zxpg', methods=['GET'])
def zxpg():        
    return render_template("jjrwfa/zxpg.html")


@app.route('/jjrwfa/jjfa', methods=['GET'])
def jjfa():        
    return render_template("jjrwfa/jjfa.html")

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

@app.route('/jjrwfa/rgfa', methods=['GET'])
def rgfa():        
    return render_template("jjrwfa/rgfa.html")

@app.route('/jjrwfa/xtfa', methods=['GET'])
def xtfa():        
    return render_template("jjrwfa/xtfa.html")

@app.route('/jjrwfa/show_jjfa', methods=['GET'])
def show_jjfa():        
    return render_template("jjrwfa/show_jjfa.html")




@app.route('/khzldy/khzl', methods=['GET'])
def khzl():        
    return render_template("khzldy/khzl.html")


@app.route('/khzldy/khzl_info', methods=['GET'])
def khzl_info():        
    return render_template("khzldy/khzl_info.html")

@app.route('/zjzxpggl/jjrw', methods=['GET'])
def jjrw():        
    return render_template("zjzxpggl/jjrw.html")


@app.route('/zjzxpggl/yjsrw', methods=['GET'])
def yjsrw():        
    return render_template("zjzxpggl/yjsrw.html")

@app.route('/zjzxpggl/yjsrw_kspg', methods=['GET'])
def yjsrw_kspg():        
    return render_template("zjzxpggl/yjsrw_kspg.html")


@app.route('/zjzxpggl/yjjrw', methods=['GET'])
def yjjrw():        
    return render_template("zjzxpggl/yjjrw.html")

@app.route('/zjzxpggl/yjjrw_jjyy', methods=['GET'])
def yjjrw_jjyy():        
    return render_template("zjzxpggl/yjjrw_jjyy.html")

@app.route('/zxpgjl/pgjl', methods=['GET'])
def pgjl():        
    return render_template("zxpgjl/pgjl.html")

@app.route('/zxpgjl/pgjl_info', methods=['GET'])
def pgjl_info():        
    return render_template("zxpgjl/pgjl_info.html")

@app.route('/zxpggzwh/pggzwh', methods=['GET'])
def pggzwh():        
    return render_template("zxpggzwh/pggzwh.html")

@app.route('/pgzjgl/zjxxgl', methods=['GET'])
def zjxxgl():        
    return render_template("pgzjgl/zjxxgl.html")

@app.route('/pgzjgl/new_zjxxgl', methods=['GET'])
def new_zjxxgl():        
    return render_template("pgzjgl/new_zjxxgl.html")

@app.route('/pgzjgl/edit_zjxxgl', methods=['GET'])
def edit_zjxxgl():        
    return render_template("pgzjgl/edit_zjxxgl.html")

@app.route('/pgzjgl/show_zjxxgl', methods=['GET'])
def show_zjxxgl():        
    return render_template("pgzjgl/show_zjxxgl.html")

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
