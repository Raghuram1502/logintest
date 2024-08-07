import jwt
from flask import Flask,request,redirect,render_template
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import login_user
from flask_login import UserMixin



class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)

class Blocks(db.Model):
  id = mapped_column(Integer,autoincrement=True, primary_key=True)
  value = mapped_column(String(100),nullable=False)

class Users(UserMixin):
  id = mapped_column(Integer,autoincrement=True, primary_key=True)
  email = mapped_column(String(50),nullable=False)
  name = mapped_column(String(50),nullable=False)
  password = mapped_column(String(20),nullable=False)
  
with app.app_context():
    db.create_all()

@app.route("/")
def home():
  return render_template("login.html")

@app.route("/register",methods = ["POST"])
def register():
  name = request.form.get("name")
  email = request.form.get("email")
  password = request.form.get("password")
  x = Users(name = name,email = email,password = password)
  db.session.add(x)
  db.session.commit()
  return render_template("index.html")
  

@app.route("/login",methods=["POST"])
def login():
  email = request.form.get("email")
  password = request.form.get("password")
  user = Users.query.filter_by(email=email).first()
  login_user(user) 
  return "ok"


@app.route("/add",methods=["POST"])
def add():
  value = request.form.get("value")
  x = Blocks(value = value)
  db.session.add(x)
  db.session.commit()
  return redirect("index.html")

@app.route("/update/<int:id>",methods = ["POST"])
def update(id):
  block = db.get_or_404(Blocks,id)
  data = request.form.get("value")
  block.value = data
  db.session.commit()
  return redirect("container.html")

@app.route("/delete/<int:id>",methods = ["POST"])
def delete(id):
  block = db.get_or_404(Blocks,id)
  db.session.delete(block)
  db.session.commit()
  return redirect("container.html")
  
@app.route("/getallblocks",methods = ["GET"])
def allblocks():
  blocks = db.session.execute(db.select(Blocks)).scalars()
  return render_template("container.html",blocks=blocks)


  

