#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/5/16
from flask import render_template,redirect,url_for,flash,request,session
from myapp.home.forms import RegisterForm,UserLoginForm,UserInfoForm,User_Change_pwdForm,AddComment,AddMoviecol
from werkzeug.utils import secure_filename
import os
import myapp
from . import home  #从当前模块导入home蓝图的对象
from werkzeug.security import generate_password_hash
from myapp.models import User,Userlog,Comment,Moviecol,Movie,Preview,Tag
import uuid
import datetime
from functools import wraps
def user_login_req(f,*args,**kwargs):   #登陆装饰器
    @wraps(f)
    def decorated_functions(*args,**kwargs):
        if 'user' not in session:
            return redirect(url_for('home.login',next=request.url))
        return f(*args,**kwargs)
    return decorated_functions

def change_filename(filename):
    fileinfo=os.path.splitext(filename)
    filename=datetime.datetime.now().strftime('%Y%m%d%H%M%S')+str(uuid.uuid4().hex)+fileinfo[-1]
    return filename


@home.route('/<int:page>/',methods=['GET'])   #主页
def movie(page):
    tag = Tag.query
    page_data = Movie.query
    tid = request.args.get("tid", 0)
    if int(tid) != 0:
        page_data = page_data.filter_by(tag_id=int(tid))
    star = request.args.get("star", 0)
    if int(star) != 0:
        page_data = page_data.filter_by(star=int(star))
    time = request.args.get("time", 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(
                Movie.addtime.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.addtime.asc()
            )
    pm = request.args.get("pm", 0)
    if int(pm) != 0:
        if int(pm) == 1:
            page_data = page_data.order_by(
                Movie.playnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.playnum.asc()
            )
    cm = request.args.get("cm", 0)
    if int(cm) != 0:
        if int(cm) == 1:
            page_data = page_data.order_by(
                Movie.commentnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.commentnum.asc()
            )
    if page is None:
        page = 1
    page_data = page_data.paginate(page=page, per_page=8)
    p = dict(
        tid=tid,
        star=star,
        time=time,
        pm=pm,
        cm=cm,
    )
    return render_template('home/movie.html',tag=tag,p=p,page_data=page_data)

@home.route('/login/',methods=['GET','POST'])  #登陆界面
def login():
    form=UserLoginForm()
    if form.validate_on_submit():
        data=form.data
        user_login_by_name=User.query.filter_by(name=data['name']).first()
        user_login_by_phone=User.query.filter_by(phone=data['name']).first()
        user_login_by_email=User.query.filter_by(email=data['name']).first()
        if not user_login_by_name and not user_login_by_email and not user_login_by_phone:
            flash('该账号不存在','err')
            return redirect(url_for('home.login'))
        if user_login_by_name:
            if  not user_login_by_name.user_check_pwd(data['pwd']):
                flash('密码错误','err')
                return redirect(url_for('home.login'))
            session['user']=user_login_by_name.name
            session['user_id']=user_login_by_name.id
            login_log_list=Userlog(
                user_id=int(session['user_id']),
                ip=request.remote_addr,
                addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            )
            Userlog.login_log(login_log_list)          #加入日志
            return redirect(url_for('home.user',id=session['user_id']))
        if user_login_by_email:
            if  not user_login_by_email.user_check_pwd(data['pwd']):
                flash('密码错误','err')
                return redirect(url_for('home.login'))
            session['user']=user_login_by_email.name
            session['user_id']=user_login_by_email.id
            login_log_list=Userlog(
                user_id=int(session['user_id']),
                ip=request.remote_addr,
                addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            )
            Userlog.login_log(login_log_list)          #加入日志
            return redirect(url_for('home.user',id=session['user_id']))
        if user_login_by_phone:
            if  not user_login_by_phone.user_check_pwd(data['pwd']):
                flash('密码错误','err')
                return redirect(url_for('home.login'))
            session['user']=user_login_by_phone.name
            session['user_id']=user_login_by_phone.id
            login_log_list=Userlog(
                user_id=int(session['user_id']),
                ip=request.remote_addr,
                addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            )
            Userlog.login_log(login_log_list)          #加入日志
            return redirect(url_for('home.user',id=session['user_id']))

    return render_template('home/login.html',form=form)



@home.route('/logout/')   #退出登陆
def logout():
    session.pop('user',None)
    session.pop('user_id',None)
    return redirect(url_for('home.login'))

@home.route('/register/',methods=['GET','POST'])  #会员注册
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        data=form.data
        user=User(
            name=data['name'],
            pwd=generate_password_hash(data['pwd']),
            email=data['email'],
            phone=data['phone'],
            uuid=str(datetime.datetime.now)+uuid.uuid4().hex,
        )
        if User.register(user):
            flash('注册成功！','ok')
            return redirect(url_for('home.login'))
    return render_template('home/register.html',form=form)


@home.route('/user/<int:id>/',methods=['GET','POST'])   #会员中心
@user_login_req
def user(id):
    form=UserInfoForm()
    user=User.query.filter_by(id=id).first()
    if form.validate_on_submit():
        data=form.data
        user.info=data['info']
        if User.user_edit(id,user):
            flash('信息修改成功！','ok')
            return redirect(url_for('home.user',id=session['user_id']))
    return render_template('home/user.html',form=form,user=user)

@home.route('/changepwd/<int:id>/',methods=['GET','POST'])  #修改密码
@user_login_req
def changepwd(id):
    form=User_Change_pwdForm()
    user=User.query.filter_by(id=id).first()
    if form.validate_on_submit():
        data=form.data
        if not User.user_check_old_pwd(session['user'],data['old_pwd']):
            flash('旧密码输入错误！','err')
        if data['new_pwd']!= data['new_pwd_again']:
            flash('两次输入的密码不一致','err')
        if user.user_check_pwd(data['old_pwd']) and data['new_pwd']== data['new_pwd_again'] and User.change_user(session['user'],data['old_pwd'],data['new_pwd']):
            flash('密码修改成功！请重新登陆','ok')
            return redirect(url_for('home.logout'))
    return render_template('home/changepwd.html',form=form)

@home.route('/comments/<int:id>/<int:page>/',methods=['GET','POST'])  #评论
@user_login_req
def comments(id,page):
    if page is None:
        page=1
    per_page_date=30          #每页显示数据
    if page is None:
        page=1
    last_page=0
    next_page=page+1
    pre_page=page-1
    if int(Comment.query.filter_by(user_id=id).count())/per_page_date==0:
        last_page=int(Comment.query.filter_by(user_id=id).count()/per_page_date)
    else:
        last_page=int(Comment.query.filter_by(user_id=id).count()/per_page_date)+1
    comments_list=Comment.query.order_by(
        Comment.addtime.desc()
    ).filter_by(user_id=id).all()
    face=User.query.filter_by(id=id).first()
    return render_template('home/comments.html',page=page,comments_list=comments_list,face=face,last_page=last_page,next_page=next_page,pre_page=pre_page)

@home.route('/loginlog/<int:id>/<int:page>/')     #登陆日志
@user_login_req
def loginlog(id,page):
    per_page_date=30          #每页显示数据
    if page is None:
        page=1
    next_page=page+1
    pre_page=page-1
    if int(Userlog.query.count())/per_page_date==0:
        last_page=int(Userlog.query.filter_by(user_id=id).count()/per_page_date)
    else:
        last_page=int(Userlog.query.filter_by(user_id=id).count()/per_page_date)+1
    login_log=Userlog.query.order_by(
        Userlog.addtime.desc()
    ).filter_by(user_id=id).all()[(page-1)*per_page_date:page*per_page_date]

    return render_template('home/loginlog.html',id=id,login_log=login_log,page=page,next_page=next_page,last_page=last_page,pre_page=pre_page)

@home.route('/moviecol/<int:id>/<int:page>/',methods=['GET','POST'])     #电影收藏
@user_login_req
def moviecol(id,page):
    next_page=last_page=pre_page=0
    moviecol_list=Moviecol.query.filter_by(user_id=id).all()
    movie_detail=[]
    if moviecol_list:
        for moviecol in moviecol_list:
            movie_url=Movie.query.filter_by(id=moviecol.movie_id).all()
            movie_detail.append(movie_url)
        for movie in movie_detail:
            for detail in movie:
                per_page_date=30          #每页显示数据
                if page is None:
                    page=1
                next_page=page+1
                pre_page=page-1
                if int(Movie.query.filter_by(id=moviecol.movie_id).count())/per_page_date==0:
                    last_page=int(Movie.query.filter_by(id=moviecol.movie_id).count()/per_page_date)
                else:
                    last_page=int(Movie.query.filter_by(id=moviecol.movie_id).count()/per_page_date)+1
    return render_template('home/moviecol.html',movie_detail=movie_detail,page=page,next_page=next_page,last_page=last_page,pre_page=pre_page)

@home.route('/play/<int:id>/<int:page>',methods=['GET','POST'])   #电影播放
def play(id,page):
    movie=Movie.query.filter_by(id=id).first()
    if movie:
        movie.playnum=int(movie.playnum)+1
        Movie.add_comment_or_play(movie)
        form=AddComment()
        if form.validate_on_submit():
            if not session['user_id']:
                return redirect(url_for('home.login'))
            data=form.data
            if data['content']:
                comment=Comment(
                    user_id=session['user_id'],
                    movie_id=id,
                    addtime=datetime.datetime.now(),
                    content=data['content']
                )
                if Comment.addcomment(comment):
                    flash("添加评论成功！",'ok')
                    movie.commentnum=int(movie.commentnum)+1
                    Movie.add_comment_or_play(movie)
                    return redirect(url_for('home.play',id=id,page=page))
        shoucang=AddMoviecol()
        if shoucang.validate_on_submit():
            if not Moviecol.query.filter_by(user_id=session['user_id'],movie_id=id).count():
                if Moviecol.moviecol_add(session['user_id'],id):
                    flash("收藏成功！",'ok')
                    return redirect(url_for('home.play',id=id,page=page))
            else:
                if Moviecol.moviecol_del_by_user(session['user_id'],id):
                    flash("取消收藏！",'err')
                    return redirect(url_for('home.play',id=id,page=page))
        pre_page_date=20     #每页20条数据
        comment_count=Comment.query.filter_by(movie_id=id).count() #评论总数
        page_data=Movie.query.filter_by(id=id).first_or_404()
        tag=Tag.query.filter_by(id=page_data.tag_id).first_or_404()
        tag_name=tag.name
        if page is None:
            page=1
        next_page=page+1
        pre_page=page-1
        data=Comment.comment_query(id=id,per_page=page,page_count=pre_page_date)
        if int(comment_count/pre_page_date)==0:
            last_page=int(comment_count/pre_page_date)
        else:
            last_page=int(comment_count/pre_page_date)+1
        comment=[]
        for v in data:
            comment.append({
                'id':v[0],
                'user_name':v[1],
                'movie_title':v[2],
                'content':v[3],
                'addtime':v[4],
                'face':v[5]
            })
    return render_template('home/play.html',shoucang=shoucang,id=id,form=form,page_data=page_data,tag_name=tag_name,comment=comment,last_page=last_page,page=page,next_page=next_page,pre_page=pre_page,comment_count=comment_count)

@home.route('/banner/')   #预告
def banner():
    preview_url=Preview.query.all()           #预告对象 列表形式
    return render_template('home/banner.html',preview_url=preview_url)

@home.route('/search/<int:page>/',methods=['GET'])       #搜索结果
def search(page):
    key=request.args.get('key','')
    if page is None:
        page=1
    page_data=Movie.query.filter(
        Movie.title.ilike('%'+key+'%')
    ).paginate(page=page,per_page=10)
    movie_count=Movie.query.filter(
        Movie.title.ilike('%'+key+'%')
    ).count()
    return render_template('home/search.html',page_data=page_data,key=key,movie_count=movie_count)

