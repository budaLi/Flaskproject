#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/5/16
from . import admin
from flask import render_template,redirect,url_for,flash,session,request,get_flashed_messages,abort
from myapp.admin.forms import LoginForm,MovieForm,TagForm,UserForm,PreviewForm,Change_pwdForm,AuthForm,RoleForm,AdminForm
from myapp.models import Admin,Tag,Movie,User,Preview,Comment,Moviecol,Oplog,Adminlog,Userlog,Auth,Role
from  functools import wraps
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
import datetime
import uuid
import myapp


def admin_login_req(f,*args,**kwargs):   #登陆装饰器
    @wraps(f)
    def decorated_functions(*args,**kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin.login',next=request.url))
        return f(*args,**kwargs)
    return decorated_functions

def admin_auth(f,*args,**kwargs):   #权限访问装饰器
    @wraps(f)
    def decorated_functions(*args,**kwargs):
        url=request.url_rule           #为Rule对象 <class 'werkzeug.routing.Rule'>
        auth_list=[]
        admin= Admin.query.filter_by(id=session['admin_id']).first()     #查出admin id
        role=Role.query.filter_by(id=admin.role_id).first()
        auth_list=list(map(lambda v:int(v),role.auths.split(',')))        #将角色对应的权限转换为列表
        for v in auth_list:
             auth=Auth.query.filter_by(id=v).first()
             if auth:               #不写报错。。
                auth_list.append(auth.url)
        if str(url) not in auth_list:
            abort(404)
        return f(*args,**kwargs)
    return decorated_functions


@admin.context_processor
def tpl_extra():   #上下文处理器
    data=dict(
        online_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    return data

# def admin_op_log(f,*args,**kwargs):    #管理员操作记录装饰器
#     @wraps(f)
#     def op_log_add(*args,**kwargs):
#         op_log_list=Oplog(
#             admin_id=1,
#             addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#             ip=request.remote_addr,
#             reason=args
#         )
#         return f(*args,**kwargs)
#     return op_log_add

# def Pagenate(all_data,per_data,cur_page):       #分页        总数据和每页显示的数据,当前页
#     has_preview=True
#     has_next=True
#     if all_data/per_data==0:
#         page_num=all_data/per_data
#     else:
#         page_num=all_data/per_data+1
#     last_page=int(page_num)-1
#     if cur_page==0:
#         has_preview=False
#     if cur_page==last_page:
#         has_next=False
#     return page_num
def change_filename(filename):
    fileinfo=os.path.splitext(filename)
    filename=datetime.datetime.now().strftime('%Y%m%d%H%M%S')+str(uuid.uuid4().hex)+fileinfo[-1]
    return filename


@admin.route('/',methods=['GET','POST'])             #登陆管理
def login():
    form=LoginForm()
    if form.validate_on_submit():
        data=form.data
        admin=Admin.query.filter_by(name=data['account']).first()
        if  not admin.check_pwd(data['pwd']):
            flash('密码错误','err')
            return redirect(url_for('admin.login'))
        session['admin']=data['account']
        session['admin_id']=admin.id
        login_log_list=Adminlog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
        )
        Adminlog.login_log(login_log_list)          #加入日志
        return redirect(url_for('admin.index'))
    return render_template('admin/login.html',form=form)

@admin.route('/logout/')        #退出登陆
@admin_login_req
def logout():
    session.pop('admin')
    return redirect(url_for('admin.login'))



@admin.route('/admin_add/',methods=['GET','POST'])           #添加管理员
@admin_login_req
@admin_auth
def admin_add():
    form=AdminForm()
    if form.validate_on_submit():
        data=form.data
        admin_count=Admin.query.filter_by(name=data['name']).count()
        if admin_count==1:
            flash('管理员名称重复!','err')
            return redirect(url_for('admin.admin_add'))
        admin=Admin(
            name=data['name'],
            pwd=generate_password_hash(data['pwd']),
            is_super=1,
            role_id=data['role']
        )
        if data['pwd']!=data['pwd_again']:
            flash('两次输入的密码不一致!','err')
            return redirect(url_for('admin.admin_add'))
        if  Admin.admin_add(admin):
            op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="添加管理员: %s "%data['name']
        )
            Oplog.add_log(op_log_list)          #加入日志
            flash('添加管理员成功!','ok')
            return redirect(url_for('admin.admin_list',page=1))
    return render_template('admin/admin_add.html',form=form)

@admin.route('/admin_list/<int:page>/',methods=['GET','POST'])        #管理员列表
@admin_login_req
@admin_auth
def admin_list(page):
    if page is None:
        page=1
    page_data=Admin.query.order_by(
        Admin.id.asc()
    ).paginate(page=page,per_page=10)
    if page_data:
        role=[]
        for v in page_data.items:
            roles=Role.query.filter_by(id=v.role_id).first()
            if roles:
                role.append(Role.query.filter_by(id=v.role_id).first().name)
    return render_template('admin/admin_list.html',page_data=page_data,role=role)

@admin.route('/adminloginlog_list/<int:page>/',methods=['GET'])       #管理员登陆日志列表
@admin_login_req
@admin_auth
def adminloginlog_list(page):
    if page is None:
        page=1
    page_data=Adminlog.query.order_by(Adminlog.addtime.desc()
    ).paginate(page=page,per_page=50)
    return render_template('admin/adminloginlog_list.html',page_data=page_data)

@admin.route('/auth_add/',methods=['GET','POST'])               #添加权限
@admin_login_req
@admin_auth
def auth_add():
    form=AuthForm()
    if form.validate_on_submit():
        data=form.data
        auth=Auth(
            name=data['name'],
            url=data['url']
        )
        auth_count=Auth.query.filter_by(name=data['name']).count()
        if auth_count==1:
            flash('权限名称重复!','err')
            return redirect(url_for('admin.auth_add'))
        if Auth.auth_add(auth):
            op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="添加权限: %s "%data['name']
        )
            Oplog.add_log(op_log_list)          #加入日志
            flash('添加权限成功!','ok')
            return redirect(url_for('admin.auth_add'))
    return render_template('admin/auth_add.html',form=form)

@admin.route('/auth_list/<int:page>/',methods=['GET'])              #权限列表
@admin_login_req
@admin_auth
def auth_list(page):
    if page is None:
        page=1
    page_data=Auth.query.order_by(
        Auth.addtime.desc()
    ).paginate(page=page,per_page=10)
    return render_template('admin/auth_list.html',page_data=page_data)

@admin.route('/auth_del/<int:id>/',methods=['POST','GET'])
@admin_login_req
@admin_auth
def auth_del(id):                           #删除权限
    auth=Auth.query.filter_by(id=id).first()
    if Auth.auth_del(id):
        flash('权限删除成功！','ok')
        op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="删除权限：%s"%(auth.name)
        )
        Oplog.add_log(op_log_list)          #加入日志
    return redirect(url_for('admin.auth_list',page=1))

@admin.route('/auth_edit/<int:id>/',methods=['GET','POST'])
@admin_login_req
@admin_auth
def auth_edit(id):                        #编辑权限
    form=AuthForm()
    auth=Auth.query.filter_by(id=id).first()
    if form.validate_on_submit():
        data=form.data
        auth_name_count=Auth.query.filter_by(name=data['name']).count()
        # if auth.name==data['name'] and auth_name_count==1:
        #     flash("权限名已经存在！",'err')
        #     return redirect(url_for('admin.auth_edit',id=id))
        if Auth.auth_edit(id,data['name'],data['url']):
            op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="修改权限名:%s->%s 权限地址:%s->%s" % (auth.name,data['name'],auth.url,data['url'])
        )
            Oplog.add_log(op_log_list)          #加入日志
            flash('编辑成功！','ok')
            return redirect(url_for('admin.auth_list',page=1))
    return render_template('admin/auth_edit.html',id=id,form=form,auth=auth)

@admin.route('/comment_list/<int:page>/',methods=['GET'])          #评论列表
@admin_login_req
@admin_auth
def comment_list(page):
    per_page_data=10
    if page is None:
        page=1
    next_page=page+1
    pre_page=page-1
    data=Comment.comment_query(id=None,per_page=page,page_count=per_page_data)   #每页100条数据
    if int(Comment.query.count()/per_page_data)==0:
        last_page=int(Comment.query.count()/per_page_data)
    else:
        last_page=int(Comment.query.count()/per_page_data)+1
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

    return render_template('admin/comment_list.html',comment=comment,last_page=last_page,page=page,next_page=next_page,pre_page=pre_page)

@admin.route('/comment_del/<int:id>/',methods=['POST','GET'])
@admin_login_req
@admin_auth
def comment_del(id):        #删除评论
    comment=Comment.query.filter_by(id=id).first()
    user_name=User.query.filter_by(id=comment.user_id).first()
    movie_name=Movie.query.filter_by(id=comment.movie_id).first()
    if Comment.comment_del(id):
        op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="删除 %s 对电影 %s 的评论：%s 成功"%(user_name,movie_name,comment.content)
        )
        Oplog.add_log(op_log_list)          #加入日志
        flash('评论删除成功！','ok')
        return redirect(url_for('admin.comment_list',page=1))
    return redirect(url_for('admin.comment_list',page=1))

@admin.route('/movie_add/',methods=['POST','GET'])
@admin_login_req
@admin_auth
def movie_add():            #添加电影
    form=MovieForm()
    if form.validate_on_submit():
        data=form.data
        file_url=secure_filename(form.url.data.filename)
        file_logo=secure_filename(form.logo.data.filename)
        if not os.path.exists(myapp.app.config['UP_DIR']):
            os.makedirs(myapp.app.config['UP_DIR'])
            os.chmod(myapp.app.config['UP_DIR'],str('rw'))
        url=change_filename(file_url)
        logo=change_filename(file_logo)
        form.url.data.save(myapp.app.config['UP_DIR']+url)
        form.logo.data.save(myapp.app.config['UP_DIR']+logo)
        movie=Movie(
            title=data['title'],
            url=url,
            info=data['info'],
            logo=logo,
            star=int(data['star']),
            playnum=0,
            commentnum=0,
            tag_id=int(data['tag_id']),
            area=data['area'],
            releasetime=data['releasetime'],
            length=str(data['length']))
        if Movie.movie_add(movie):
            op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="添加电影 %s成功"%(data['title'])
        )
            Oplog.add_log(op_log_list)          #加入日志
            flash('添加电影成功','ok')
    return render_template('admin/movie_add.html',form=form)


@admin.route('/movie_edit/<int:id>/',methods=['GET','POST'])
@admin_login_req
@admin_auth
def movie_edit(id):                        #编辑电影
    form=MovieForm()
    movie=Movie.query.get_or_404(id)
    if form.validate_on_submit():
        file_url=secure_filename(form.url.data.filename)
        file_logo=secure_filename(form.logo.data.filename)
        url=change_filename(file_url)
        logo=change_filename(file_logo)
        data=form.data
        form.info.data=data['info']
        if not os.path.exists(myapp.app.config['UP_DIR']):
            os.makedirs(myapp.app.config['UP_DIR'])
            os.chmod(myapp.app.config['UP_DIR'],int('rw'))
        url=change_filename(file_url)
        logo=change_filename(file_logo)
        form.url.data.save(myapp.app.config['UP_DIR']+url)
        form.logo.data.save(myapp.app.config['UP_DIR']+logo)
        if data:
            movie=Movie(
            id=int(id),
            title=data['title'],
            url=url,
            info=data['info'],
            logo=logo,
            star=int(data['star']),
            tag_id=int(data['tag_id']),
            area=data['area'],
            length=int(data['length']),
            releasetime=data['releasetime'])
            if Movie.movie_edit(id,movie):
                op_log_list=Oplog(
                admin_id=int(session['admin_id']),
                addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                ip=request.remote_addr,
                reason="编辑电影: %s 成功"%data['title'])
                Oplog.add_log(op_log_list)          #加入日志
                flash('电影编辑成功！','ok')
                return redirect(url_for('admin.movie_list',page=1))
        return redirect(url_for('admin.movie_list',page=1))
    return render_template('admin/movie_edit.html',id=id,form=form,movie=movie)

@admin.route('/movie_list/<int:page>/',methods=['GET','POST'])
@admin_login_req
@admin_auth
def movie_list(page):        #电影列表
    per_page_date=30          #每页显示数据
    if page is None:
        page=1
    page_data=Movie.query.order_by(
        Movie.id.asc()
    ).paginate(page=page,per_page=per_page_date)
    tag_name=[]
    for v in page_data.items:      #v为movie对象
        tag=Tag.query.filter_by(id=int(v.tag_id)).first()
        tag_name.append(tag.name)
    return render_template('admin/movie_list.html',page_data=page_data,tag_name=tag_name)

@admin.route('/movie_del/<int:id>/',methods=['POST','GET'])
@admin_login_req
@admin_auth
def movie_del(id):                           #删除电影
    movie=Movie.query.filter_by(id=id).first_or_404()
    if Movie.movie_del(id):
        op_log_list=Oplog(
                admin_id=int(session['admin_id']),
                addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                ip=request.remote_addr,
                reason="删除电影: %s 成功"%movie.title)
        Oplog.add_log(op_log_list)          #加入日志
        flash('电影删除成功！','ok')
    return redirect(url_for('admin.movie_list',page=1))

@admin.route('/moviecol_list/<int:page>/',methods=['GET','POST'])
@admin_login_req
@admin_auth
def moviecol_list(page):        #收藏电影列表
    per_page_date=30
    if page is None:
        page=1
    next_page=page+1
    pre_page=page-1
    if int(Moviecol.query.count()/per_page_date)==0:
        last_page=int(Comment.query.count()/per_page_date)
    else:
        last_page=int(Comment.query.count()/per_page_date)+1
    data=Moviecol.moviecol_query(per_page=page,page_count=per_page_date)
    moviecol=[]
    for v in data:
        moviecol.append({
            'id':v[0],
            'user_name':v[1],
            'movie_title':v[2],
            'addtime':v[3]
        })
    return render_template('admin/moviecol_list.html',moviecol=moviecol,page=page,last_page=last_page,next_page=next_page,pre_page=pre_page)

@admin.route('/moviecol_del/<int:id>/',methods=['GET','POST'])        #删除收藏
@admin_login_req
@admin_auth
def moviecol_del(id):
    movie=Moviecol.query.filter_by(id=id).first_or_404()
    movie_name=Movie.query.filter_by(id=movie.movie_id).first_or_404()
    if Moviecol.moviecol_del(id):
        op_log_list=Oplog(
                admin_id=int(session['admin_id']),
                addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                ip=request.remote_addr,
                reason="删除收藏: %s 成功")%movie_name.title
        Oplog.add_log(op_log_list)          #加入日志
        flash('删除收藏成功','ok')
    else:
        flash('删除收藏失败','err')
    return redirect(url_for('admin.moviecol_list',page=1))

@admin.route('/oplog_list/<int:page>/',methods=['GET','POST'])       #操作日志列表
@admin_login_req
@admin_auth
def oplog_list(page):
    if page is None:
        page=1
    page_data=Oplog.query.order_by(
        Oplog.addtime.desc()
    ).paginate(page=page,per_page=50)
    return render_template('admin/oplog_list.html',page_data=page_data)


@admin.route('/preview_add/',methods=['GET','POST'])           #添加预告
@admin_login_req
@admin_auth
def preview_add():
    form=PreviewForm()
    if form.validate_on_submit():
        data=form.data
        file_url=secure_filename(form.url.data.filename)
        if not os.path.exists(myapp.app.config['UP_DIR']):
            os.makedirs(myapp.app.config['UP_DIR'])
            os.chmod(myapp.app.config['UP_DIR'],int('rw'))
        url=change_filename(file_url)
        form.url.data.save(myapp.app.config['UP_DIR']+url)
        preview=Preview(
            title=data['title'],
            logo=url
        )
        preview_list=Preview.query.filter_by(title=data['title']).count()
        if preview_list:
            flash("预告名称重复！",'err')
            return render_template('admin/preview_add.html',form=form)
        if Preview.preview_add(preview):
            flash('添加预告成功','ok')
            return render_template('admin/preview_add.html',form=form)
    return render_template('admin/preview_add.html',form=form)

@admin.route('/preview_list/<int:page>/',methods=['GET','POST'])       #预告列表
@admin_login_req
@admin_auth
def preview_list(page):
    if page is None:
        page=1
    page_data=Preview.query.order_by(
        Preview.id.asc()
    ).paginate(page=page,per_page=50)
    return render_template('admin/preview_list.html',page_data=page_data)

@admin.route('/preview_edit/<int:id>/',methods=['GET','POST'])   #编辑预告
@admin_login_req
@admin_auth
def preview_edit(id):
    form=PreviewForm()
    preview_old=Preview.query.filter_by(id=id).first()
    if form.validate_on_submit():
        data=form.data
        file_url=secure_filename(form.url.data.filename)
        if not os.path.exists(myapp.app.config['UP_DIR']):
            os.makedirs(myapp.app.config['UP_DIR'])
            os.chmod(myapp.app.config['UP_DIR'],str('rw'))
        url=change_filename(file_url)
        form.url.data.save(myapp.app.config['UP_DIR']+url)
        preview=Preview.query.filter_by(title=data['title']).count()
        if preview:
            flash('预告名称重复','err')
            return redirect(url_for('admin.preview_edit',id=id))
        preview_now=Preview(
            id=id,
            title=data['title'],
            logo=url
        )
        if Preview.preview_edit(id,preview_now):
            op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="编辑预告 %s成功"%(id)
        )
            Oplog.add_log(op_log_list)          #加入日志
            flash('编辑预告成功','ok')
            return redirect(url_for('admin.preview_edit',id=id))
    return render_template('admin/preview_edit.html',form=form,preview_old=preview_old)

@admin.route('/preview_del/<int:id>/',methods=['POST','GET'])
@admin_login_req
@admin_auth
def preview_del(id):                           #删除预告
    preview=Preview.query.filter_by(id=id).first_or_404()
    if Preview.preview_del(id):
        op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="删除预告：id:%s name :%s 成功"%(id,preview.title)
        )
        Oplog.add_log(op_log_list)          #加入日志
        flash('预告删除成功！','ok')
    return redirect(url_for('admin.preview_list',page=1))


@admin.route('/pwd/',methods=['GET','POST'])
@admin_login_req
def pwd():                    #修改密码
    form=Change_pwdForm()
    if form.validate_on_submit():
        data=form.data
        if not Admin.check_old_pwd(session['admin'],data['old_pwd']):
            op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="修改密码失败：旧密码输入错误"
        )
            Oplog.add_log(op_log_list)          #加入日志
            flash('旧密码输入错误！','err')
        if data['new_pwd']!= data['new_pwd_again']:
            flash('两次输入的密码不一致','err')
            op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="修改密码失败：两次输入的密码不一致"
        )
            Oplog.add_log(op_log_list)          #加入日志
        if Admin.check_old_pwd(session['admin'],data['old_pwd']) and data['new_pwd']== data['new_pwd_again'] and Admin.change_admin(session['admin'],data['old_pwd'],data['new_pwd']):
            flash('密码修改成功！请重新登陆','ok')
            op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="修改密码成功"
        )
            Oplog.add_log(op_log_list)          #加入日志
            return redirect(url_for('admin.logout'))
    return render_template('admin/pwd.html',form=form)

@admin.route('/role_add/',methods=['GET','POST'])
@admin_login_req                  #添加角色
@admin_auth
def role_add():
    form=RoleForm()
    if form.validate_on_submit():
        data=form.data
        roles=Role.query.filter_by(name=data['name']).count()
        if roles==1:
            flash('角色名称重复！','err')
            op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="添加角色: %s 出错 原因：名称重复"%(data['name'])
        )
            Oplog.add_log(op_log_list)          #加入日志
            return redirect(url_for('admin.role_add'))
        role=Role(
            name=data['name'],
            auths=','.join(map(lambda v:str(v),data['auths']))
        )
        if Role.role_add(role):
            op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="添加角色: %s 赋予权限: %s"%(data['name'],data['auths'])
        )
            Oplog.add_log(op_log_list)          #加入日志
            flash('添加角色成功','ok')
            return redirect(url_for('admin.role_add'))
    return render_template('admin/role_add.html',form=form)

@admin.route('/role_list/<int:page>/',methods=['GET','POST'])
@admin_login_req
@admin_auth
def role_list(page):           #角色列表
    if page is None:
        page=1
    page_data=Role.query.order_by(
        Role.id.asc()
    ).paginate(page=page,per_page=10)
    return render_template('admin/role_list.html',page_data=page_data)

@admin.route('/role_edit/<int:id>/',methods=['GET','POST'])
@admin_login_req
@admin_auth
def role_edit(id):                        #编辑角色
    form=RoleForm()
    role=Role.query.filter_by(id=id).first()
    if request.method=='GET':
        form.auths.data=list(map(lambda v:int(v),role.auths.split(',')))          #很重要。。
    if form.validate_on_submit():
        data=form.data
        auths=','.join(map(lambda v:str(v),data['auths']))
        if Role.role_edit(id,data['name'],auths):
            op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="修改角色:%s->%s 角色权限:%s->%s" % (role.name,data['name'],role.auths,data['auths'])
        )
            Oplog.add_log(op_log_list)          #加入日志
            flash('编辑成功！','ok')
            return redirect(url_for('admin.role_list',page=1))
    return render_template('admin/role_edit.html',id=id,form=form,role=role)

@admin.route('/role_del/<int:id>/',methods=['POST','GET'])
@admin_login_req
@admin_auth
def role_del(id):                           #删除角色
    role=Role.query.filter_by(id=id).first()
    if Role.role_del(id):
        flash('角色删除成功！','ok')
        op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="删除标签：id:%s name :%s"%(id,role.name)
        )
        Oplog.add_log(op_log_list)          #加入日志
    return redirect(url_for('admin.role_list',page=1))


@admin.route('/tag_add/',methods=['POST','GET'])
@admin_login_req
@admin_auth
def tag_add():                        #添加标签
    form=TagForm()
    if form.validate_on_submit():
        data=form.data
        tag=Tag.query.filter_by(name=data['name']).count()
        if tag==1:
            flash('该标签已经存在！','err')
            return redirect(url_for('admin.tag_add'))
        if Tag.tag_add(data['name']):
            flash('添加成功！','ok')
            op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="添加标签：%s"%data['name']
        )
            Oplog.add_log(op_log_list)          #加入日志
        else:
            flash("标签名错误！",'err')
            return redirect(url_for('admin.tag_add'))
    return render_template('admin/tag_add.html',form=form)

@admin.route('/tag_del/<int:id>/',methods=['POST','GET'])
@admin_login_req
@admin_auth
def tag_del(id):                           #删除标签
    tag=Tag.query.filter_by(id=id).first()
    if Tag.tag_del(id):
        flash('标签删除成功！','ok')
        op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="删除标签：id:%s name :%s"%(id,tag.name)
        )
        Oplog.add_log(op_log_list)          #加入日志
    return redirect(url_for('admin.tag_list',page=1))


@admin.route('/tag_list/<int:page>/',methods=['GET','POST'])
@admin_login_req
@admin_auth
def tag_list(page):                       #显示标签列表
    if page is None:
        page=1
    page_data=Tag.query.order_by(
        Tag.addtime.desc()
    ).paginate(page=page,per_page=20)
    return render_template('admin/tag_list.html',page_data=page_data)


@admin.route('/tag_edit/<int:id>/',methods=['GET','POST'])
@admin_login_req
@admin_auth
def tag_edit(id):                        #编辑标签
    form=TagForm()
    tag=Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data=form.data
        tag_count=Tag.query.filter_by(name=data['name']).count()
        if  tag_count==1:
            flash("标签名已经存在！",'err')
            return redirect(url_for('admin.tag_list',page=1))
        if Tag.tag_edit(id,data['name']):
            op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="修改标签名： %s -》%s "%(tag.name,data['name'])
        )
            Oplog.add_log(op_log_list)          #加入日志
            flash('编辑成功！','ok')
            return redirect(url_for('admin.tag_list',page=1))
        return redirect(url_for('admin.tag_list',page=1))
    return render_template('admin/tag_edit.html',id=id,form=form,tag=tag)

@admin.route('/user_list/<int:page>/',methods=['GET','POST'])
@admin_login_req
@admin_auth
def user_list(page):        #会员列表
    if page is None:
        page=1
    page_data=User.query.order_by(
        User.id.asc()
    ).paginate(page=page,per_page=50)

    return render_template('admin/user_list.html',page_data=page_data)


@admin.route('/user_view/<int:id>/',methods=['GET','POST'])
@admin_login_req                #会员信息
@admin_auth
def user_view(id):
    form=UserForm()
    user_info=User.query.get_or_404(id)
    if form.validate_on_submit():
        user_info=User.query.filter_by(id=id)

    return render_template('admin/user_view.html',id=id,form=form,user_info=user_info)

@admin.route('/user_del/<int:id>/',methods=['POST','GET'])
@admin_login_req
@admin_auth
def user_del(id):                           #删除会员
    user=User.query.filter_by(id=id).first_or_404()
    if User.user_del(id):
        op_log_list=Oplog(
            admin_id=int(session['admin_id']),
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ip=request.remote_addr,
            reason="删除会员：id :%s name :%s "%(id,user.name)
        )
        Oplog.add_log(op_log_list)          #加入日志
        flash('会员删除成功！','ok')
    return redirect(url_for('admin.user_list',page=1))

@admin.route('/userloginlog_list/<int:page>/',methods=['GET'])
@admin_login_req
@admin_auth
def userloginlog_list(page):             #会员登陆日志
    if page is None:
        page=1
    page_data=Userlog.query.order_by(
        Userlog.addtime.asc()
    ).paginate(page=page,per_page=50)
    return render_template('admin/userloginlog_list.html',page_data=page_data)

@admin.route('/index/',methods=['GET'])        #主界面
@admin_login_req
def index():
    return render_template('admin/index.html')

