import os

from flask import Flask, session, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
  raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
  if session.get("uid") is None:
    links = [('注册','register'), ('登录','login')]
    return render_template("message.html", message="你好, 欢迎访问本系统，您还未登录!", title= "欢迎", links=links)
  else:
    links = [('注销','logout'),('搜索','search')]
    return render_template("message.html", message=f"你好, {session.get('uname')}! 你已经登录但本网站正在开发，所以你什么也不能做！", title= "欢迎", links=links)

@app.route("/login", methods=["GET","POST"])
def login():
  if session.get("uid") is not None:
    links = [('回到首页','index'), ('注销','logout')]
    return render_template("message.html", message=f'已经登录！', title="错误", links=links)
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
    result = db.execute("select id, username from users where username=:username and password=:password",{"username":username,"password":password}).fetchall()
    if result == []:
      links = [('回到首页','index'), ('注册','register'), ('登录','login')]
      return render_template("message.html", message="账户或密码输入错误！",title="错误", links=links)
    session["uid"] = result[0][0]
    session["uname"] = result[0][1]
    links = [('回到首页','index'), ('注销','logout')]
    return render_template("message.html", message=f"你好, {username}!", title= "登录成功", links=links)
  else:
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
  if session.get("uid") is not None:
    links = [('回到首页','index'), ('注销','logout')]
    return render_template("message.html", message=f'已经登录，无法注册，请注销！', title="错误", links=links)
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
    ret = db.execute("insert into users (username, password) values (:username, :password);",{"username":username,"password":password})
    db.commit()
    links = [('回到首页','index'), ('登录','login')]
    return render_template("message.html", message="注册成功!", title= "成功", links=links)
  else:
    return render_template("register.html")

@app.route("/logout")
def logout():
  links = [('回到首页','index'), ('登录','login'), ('注册','register')]
  if session.pop("uid", None) is None:
    return render_template("message.html", message="你可以注册或者登录", title= "你并没有登录！", links=links)

  links = [('回到首页','index'), ('登录','login'), ('注册','register')]
  return render_template("message.html", message="已经成功注销", title= "成功注销", links=links)

@app.route("/search", methods=["GET","POST"])
def search():
  links = [('回到首页','index'), ('登录','login'), ('注册','register')]
  if session.get("uid") is None:
    return render_template("message.html", message="你可以注册或者登录", title= "你并没有登录！", links=links)
  if request.method == "POST":
    year = int(request.form.get("year"))
    result = db.execute("select isbn, title, author, year, id from books where year=:year",{"year":year}).fetchall()
    return render_template('result.html', books=result)
  else:
    return render_template('search.html')
  
@app.route('/book/<id>')
def bookpage(id):
  links=[("回到首页",'index')]
  return render_template("message.html", message="暂未实现", title= f"{id}图书详情", links=links)
