#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/5/16

import datetime
from myapp import db
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import and_
# from flask_sqlalchemy import BaseQuery
# import pymysql
# app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:123@127.0.0.1:3306/movie'
# app.config['SQLALCHEMY_TRACK_MODIFACTIONS']=True
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True #设置这一项是每次请求结束后都会自动提交数据库中的变动
# app.config['SECRET_KEY']='f0db499238464e40887925ca2bf1af32'
# db=SQLAlchemy(app)
# from myapp.home import home as home_blue
# from myapp.admin import admin as admin_blue
# app.register_blueprint(home_blue)
# app.register_blueprint(admin_blue,url_prefix='/admin')

#会员表
class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),unique=True)
    pwd=db.Column(db.String(100))
    email=db.Column(db.String(100),unique=True)
    phone=db.Column(db.String(100),unique=True)
    info=db.Column(db.Text)
    face=db.Column(db.String(255),unique=True)
    addtime=db.Column(db.DATETIME,index=True,default=datetime.datetime.now)
    uuid=db.Column(db.String(255),unique=True)
    # ip=db.Column(db.String(255))
    # user_log=db.relationship('Userlog',backref='user')
    # comment=db.relationship('Comment',backref='user')
    # moviecol=db.relationship('Moviecol',backref='user')
    use_log=db.Column(db.String(255))
    comment=db.Column(db.String(255))
    moviecol=db.Column(db.String(255))
    def __repr__(self):
        return "<user %s>"%self.name
    def user_check_pwd(self,pwd):
        try:
            from werkzeug.security import check_password_hash
            return  check_password_hash(self.pwd,pwd)
        except Exception as e :
            print(e)
            return False
    def user_del(id):
        user=User.query.filter_by(id=id).first_or_404()
        db.session.delete(user)
        db.session.commit()
        return True
    def register(user):
        try:
            db.session.add(user)
            db.session.commit()
            return True
        except Exception:
            return False
    def user_edit(id,user):
        try:
            old_user=User.query.filter_by(id=id).first()
            old_user.name=user.name
            old_user.email=user.email
            old_user.phone=user.phone
            old_user.face=user.face
            old_user.info=user.info
            db.session.add(old_user)
            db.session.commit()
            return True
        except Exception:
            return False
    def user_check_old_pwd(name,old_pwd):      #根据name检测旧密码
        try:
            from werkzeug.security import check_password_hash
            user= User.query.filter_by(name=name).first()
            pwd=user.pwd
            return check_password_hash(pwd,old_pwd)
        except Exception:
            return False
    def change_user(name,old_pwd,new_pwd):         #查询管理员旧密码及更新密码
        user=User.query.filter_by(name=name).first()
        if User.user_check_old_pwd(name,old_pwd):
            try:
                from werkzeug.security import generate_password_hash
                user.pwd=generate_password_hash(new_pwd)   #更新密码
                db.session.add(user)
                db.session.commit()
                return True
            except Exception:
                return False


#会员登陆日志
class Userlog(db.Model):
    __tablename__='userlog'
    id=db.Column(db.Integer,primary_key=True)
    # user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    user_id=db.Column(db.Integer)
    ip=db.Column(db.String(100))
    addtime=db.Column(db.DATETIME,index=True,default=datetime.datetime.now)

    def __repr__(self):
        return "<Userlog %s>"%self.id
    def login_log(data):
        try:
            db.session.add(data)
            db.session.commit()
            return True
        except Exception:
            return False

#电影标签
class Tag(db.Model):
    __tablename__='tag'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),unique=True)
    addtime=db.Column(db.DATETIME,index=True,default=datetime.datetime.now)
    # movies=db.relationship('Movie',backref='tag')
    movies=db.Column(db.Integer)
    def __repr__(self):
        return "<tag %s>"%self.name
    def tag_add(name):
        try:
            tag=Tag(
                name=name,
            )
            db.session.add(tag)
            db.session.commit()
            return True
        except Exception as e:
            return False
    def tag_del(id):
        tag=Tag.query.filter_by(id=id).first_or_404()
        db.session.delete(tag)
        db.session.commit()
        return True
    def tag_edit(id,name):
        tag=Tag.query.filter_by(id=id).first_or_404()
        db.session.delete(tag)
        db.session.commit()
        tag=Tag(
            id=id,
            name=name
        )
        db.session.add(tag)
        db.session.commit()
        return True
#电影
class Movie(db.Model):
    __tablename__='movie'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),unique=True)
    url=db.Column(db.String(255),unique=True)
    info=db.Column(db.TEXT)
    logo=db.Column(db.String(255),unique=True)
    star=db.Column(db.SmallInteger)
    playnum=db.Column(db.BigInteger)
    commentnum=db.Column(db.BigInteger)
    # tag_id=db.relationship('Tage',backref='movie')
    tag_id=db.Column(db.Integer)
    area=db.Column(db.String(255))
    releasetime=db.Column(db.String(100))
    length=db.Column(db.Integer)
    addtime=db.Column(db.DATETIME,index=True,default=datetime.datetime.now)
    # comment=db.relationship('Comment',backref='movie')
    # moviecol=db.relationship('Moviecol',backref='movie')
    comment=db.Column(db.String(255))
    moviecol=db.Column(db.String(255))
    def __repr__(self):
        return str(self.title)
    def movie_add(data):
        try:
             db.session.add(data)
             db.session.commit()
             return True
        except Exception as e:
            return False
    def movie_del(id):
        movie=Movie.query.filter_by(id=id).first_or_404()
        db.session.delete(movie)
        db.session.commit()
        return True
    def movie_edit(id,data):
        try:
            movie=Movie.query.filter_by(id=id).first_or_404()
            db.session.delete(movie)
            db.session.commit()
            db.session.add(data)
            db.session.commit()
            return True
        except Exception as e:
            return False
    def add_comment_or_play(movie):
        try:
            db.session.add(movie)
            db.session.commit()
            return True
        except Exception:
            return False
#上映
class Preview(db.Model):
    __tablename__='preview'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(255),unique=True)
    logo=db.Column(db.String(255),unique=True)
    addtime=db.Column(db.DATETIME,index=True,default=datetime.datetime.now)
    def __repr__(self):
        return "preview %s"%self.title
    def preview_add(data):
        try:
            db.session.add(data)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def preview_edit(id,data):
        try:
            preview=Preview.query.filter_by(id=id).first_or_404()
            preview.id=data.id
            preview.title=data.title
            preview.logo=data.logo
            db.session.add(preview)
            db.session.commit()
            return True
        except Exception as e:
            return False
    def preview_del(id):
        preview=Preview.query.filter_by(id=id).first_or_404()
        db.session.delete(preview)
        db.session.commit()
        return True

#评论
class Comment(db.Model):
    __tablename__='comment'
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.Text)
    # movie_id=db.Column(db.Integer,db.ForeignKey('movie.id'))
    # user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    movie_id=db.Column(db.Integer)
    user_id=db.Column(db.Integer)
    addtime=db.Column(db.DATETIME,index=True,default=datetime.datetime.now)

    def __repr__(self):
        return "<Comment %s>"%self.id
    def comment_query(id,per_page,page_count):
        offset_num=(int(per_page)-1)*int(page_count)
        if id:
            try:
                sql='SELECT  `comment`.id ,`user`.name ,`movie`.title ,`comment`.content, `comment`.addtime,`user`.face' \
                    ' from `comment`,movie,`user`' \
                    ' WHERE `comment`.movie_id=movie.id and `comment`.user_id =`user`.id and `comment`.movie_id =%s ORDER BY `comment`.addtime DESC LIMIT %s offset %s  '%(id,page_count,offset_num)
                data=db.session.execute(sql)
                return data
            except Exception as e:
                return None

        else:
            try:

                sql='SELECT  `comment`.id ,`user`.name ,`movie`.title ,`comment`.content, `comment`.addtime,`user`.face' \
                    ' from `comment`,movie,`user`' \
                    ' WHERE `comment`.movie_id=movie.id and `comment`.user_id =`user`.id  ORDER BY `comment`.addtime DESC LIMIT %s offset %s  '%(page_count,offset_num)
                # data=db.session.query(Comment,Movie,User).join(Movie,and_(Comment.movie_id==Movie.id)).join(User,and_(Comment.user_id==User.id)).paginate(page=page,per_page=per_page)
                # page_data=data.paginate(page=page,per_page=per_page)
                data=db.session.execute(sql)
                return data
            except Exception as e:
                return None
    def comment_del(id):
        try:
            comment=Comment.query.filter_by(id=id).first_or_404()
            db.session.delete(comment)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def addcomment(data):
        try:
            db.session.add(data)
            db.session.commit()
            return True
        except Exception:
            return False

#电影收藏
class Moviecol(db.Model):
    __tablename__='moviecol'
    id=db.Column(db.Integer,primary_key=True)
    # movie_id=db.Column(db.Integer,db.ForeignKey('movie.id'))
    # user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    movie_id=db.Column(db.Integer)
    user_id=db.Column(db.Integer)
    addtime=db.Column(db.DATETIME,index=True,default=datetime.datetime.now)

    def __repr__(self):
        return "<moviecol %s>"%self.id

    def moviecol_query(per_page,page_count):
        try:
            offset_num=(int(per_page)-1)*int(page_count)
            sql='SELECT  `moviecol`.id ,`user`.name ,`movie`.title ,`moviecol`.addtime from `moviecol`,movie,`user` WHERE `moviecol`.movie_id=movie.id and `moviecol`.user_id =`user`.id' \
                ' LIMIT %s OFFSET %s'%(page_count,offset_num)
            moviecol=db.session.execute(sql)
            return moviecol             #返回当前页需要的数据
        except Exception as e:
            print(e)
            return None
    def moviecol_del(id):
        try:
            moviecol=Moviecol.query.filter_by(id=id).first_or_404()
            db.session.delete(moviecol)
            db.session.commit()
            return True
        except Exception as e:
            return False
    def moviecol_add(user_id,movie_id):
        if Moviecol.query.filter_by(user_id=user_id,movie_id=movie_id).count()==0:
            moviecol=Moviecol(
                user_id=user_id,
                movie_id=movie_id,
                addtime=datetime.datetime.now()
            )
            try:
                db.session.add(moviecol)
                db.session.commit()
                return True
            except Exception:
                return False
        else:
            return False
    def moviecol_del_by_user(user_id,movie_id):
        try:
            movie=Moviecol.query.filter_by(movie_id=movie_id,user_id=user_id).first_or_404()
            db.session.delete(movie)
            db.session.commit()
            return True
        except Exception as e:
            return False
#权限
class Auth(db.Model):
    __tablename__='auth'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),unique=True)
    url=db.Column(db.String(255),unique=True)
    addtime=db.Column(db.DATETIME,index=True,default=datetime.datetime.now)

    def __repr__(self):
        return "<auth %s>"%self.name
    def auth_add(data):
        try:
            db.session.add(data)
            db.session.commit()
            return True
        except Exception as e:
            return False
    def auth_del(id):
        auth=Auth.query.filter_by(id=id).first_or_404()
        db.session.delete(auth)
        db.session.commit()
        return True
    def auth_edit(id,name,url):
        try:
            auth=Auth.query.filter_by(id=id).first_or_404()
            db.session.delete(auth)
            db.session.commit()
            auth_new=Auth(
                id=id,
                name=name,
                url=url
            )
            db.session.add(auth_new)
            db.session.commit()
            return True
        except Exception:
            return False
#角色
class Role(db.Model):
    __tablename__='role'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),unique=True)
    auths=db.Column(db.String(600))
    addtime=db.Column(db.DATETIME,index=True,default=datetime.datetime.now)
    # role_id=db.relationship('Admin',backref='role')
    role_id=db.Column(db.Integer)
    def __repr__(self):
        return "<role %s>"%self.name
    def role_add(data):
        try:
            db.session.add(data)
            db.session.commit()
            return True
        except Exception as e :
            print(e)
            return False
    def role_del(id):
        role=Role.query.filter_by(id=id).first_or_404()
        db.session.delete(role)
        db.session.commit()
        return True
    def role_edit(id,name,auths):
         try:
            role=Role.query.filter_by(id=id).first_or_404()
            db.session.delete(role)
            db.session.commit()
            role_new=Role(
                id=id,
                name=name,
                auths=auths
            )
            db.session.add(role_new)
            db.session.commit()
            return True
         except Exception as e:
            return False
#管理员
class Admin(db.Model):
    __tablename__='admin'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),unique=True)
    pwd=db.Column(db.String(100))
    is_super=db.Column(db.SmallInteger)  #0是
    # role_id=db.Column(db.Integer,db.ForeignKey('role.id'))
    role_id=db.Column(db.Integer)
    addtime=db.Column(db.DATETIME,index=True,default=datetime.datetime.now)
    # admin_log=db.relationship('Adminlog',backref='admin')
    # op_log=db.relationship('Oplog',backref='admin')
    admin_log=db.Column(db.Integer)
    op_log=db.Column(db.Integer)
    def __repr__(self):
        return "<admin %s>"%self.name
    def check_pwd(self,pwd):
        from werkzeug.security import check_password_hash
        return  check_password_hash(self.pwd,pwd)
    def check_old_pwd(name,old_pwd):      #根据name检测旧密码
        from werkzeug.security import check_password_hash
        admin= Admin.query.filter_by(name=name).first()
        pwd=admin.pwd
        return check_password_hash(pwd,old_pwd)
    def change_admin(name,old_pwd,new_pwd):         #查询管理员旧密码及更新密码
        admin=Admin.query.filter_by(name=name).first()
        if Admin.check_old_pwd(name,old_pwd):
            try:
                from werkzeug.security import generate_password_hash
                admin.pwd=generate_password_hash(new_pwd)   #更新密码
                db.session.add(admin)
                db.session.commit()
                return True
            except Exception:
                return False
    def admin_add(data):
        try:
            db.session.add(data)
            db.session.commit()
            return True
        except Exception:
            return False



#管理员登陆日志
class Adminlog(db.Model):
    __tablename__='adminlog'
    id=db.Column(db.Integer,primary_key=True)
    # admin_id=db.Column(db.Integer,db.ForeignKey("admin.id"))
    admin_id=db.Column(db.Integer)
    ip=db.Column(db.String(100))
    addtime=db.Column(db.DATETIME,index=True,default=datetime.datetime.now)

    def __repr__(self):
        return "<adminlog %s>"%self.id
    def login_log(data):
        db.session.add(data)
        db.session.commit()

#操作日志
class Oplog(db.Model):
    __tablename__='oplog'
    id=db.Column(db.Integer,primary_key=True)
    # admin_id=db.Column(db.Integer,db.ForeignKey("admin.id"))
    admin_id=db.Column(db.Integer)
    ip=db.Column(db.String(100))
    reason=db.Column(db.String(600))
    addtime=db.Column(db.DATETIME,index=True,default=datetime.datetime.now)

    def __repr__(self):
        return "<oplog %s>"%self.id
    def add_log(log):
        db.session.add(log)
        db.session.commit()

if __name__=='__main__':
    # pass
    # 创建表
    db.drop_all(User)
    db.create_all(User)
    # from werkzeug.security import generate_password_hash
    # role=Admin(
    #
    #     name='李不搭',
    # pwd=generate_password_hash('zslswmz'),
    # is_super=1,
    #
    # )
    # db.session.add(role)
    # db.session.commit()
    # #
