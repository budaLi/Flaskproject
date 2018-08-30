#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/5/17
import pymysql
from flask import Flask,render_template
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:123@127.0.0.1:3306/movie'
app.config['SQLALCHEMY_TRACK_MODIFACTIONS']=True
app.config['SECRET_KEY']='f0db499238464e40887925ca2bf1af22'
app.config['UP_DIR']=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static/uploads/')
app.debug=False
db=SQLAlchemy(app)



from myapp.home import home as home_blue
from myapp.admin import admin as admin_blue
app.register_blueprint(home_blue)
app.register_blueprint(admin_blue,url_prefix='/admin')
@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'),404

