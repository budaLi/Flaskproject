#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/5/16
from flask import Blueprint


admin=Blueprint('admin',__name__)
from myapp.admin import views
