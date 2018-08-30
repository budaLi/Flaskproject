#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/5/16
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,FileField,TextAreaField
from wtforms.validators import DataRequired,ValidationError,EqualTo,Email,Regexp,Length
from myapp.models import User
class RegisterForm(FlaskForm):
    name=StringField(
        label='昵称',
        validators=[
            DataRequired("请输入昵称'！")
    ],
        description='昵称',
        render_kw={
                'class':"form-control input-lg",
                'placeholder':"请输入昵称！",
                'required':'required'
        }
    )
    pwd=PasswordField(
        label='密码',
        validators=[
            DataRequired("请输入密码！")
        ],
        description='密码',
        render_kw={
                'class':"form-control input-lg",
                'placeholder':"请输入密码！",
                'required':'required'
        }
    )
    email=StringField(
        label='邮箱',
        validators=[
            DataRequired("请输入邮箱'！"),
            Email('邮箱格式不正确！')
    ],
        description='邮箱',
        render_kw={
                'class':"form-control input-lg",
                'placeholder':"请输入邮箱！",
                'required':'required'
        }
    )
    phone=StringField(
        label='手机号',
        validators=[
            DataRequired("请输入手机号'！"),
            Regexp('1[3458]\\d{9}',message='手机格式不正确！'),
            Length(min=11, max=11, message="手机长度不正确！")
    ],
        description='手机号',
        render_kw={
                'class':"form-control input-lg",
                'placeholder':"请输入手机号！",
                'required':'required'
        }
    )
    pwd_again=PasswordField(
        label='请输入确认密码',
        validators=[
            DataRequired("请输入确认密码！")
        ],
        description='确认密码',
        render_kw={
                'class':"form-control input-lg",
                'placeholder':"请输入确认密码！",
                'required':'required'
        }
    )
    submit=SubmitField(
        label='注册',
        render_kw={
            'class':"btn btn-lg btn-success btn-block",
        }

    )
    def validate_name(self,field):
        name=field.data
        admin=User.query.filter_by(name=name).count()
        if admin==1:
            raise ValidationError("该昵称已经被注册！")
    def validate_email(self,field):
        email=field.data
        admin=User.query.filter_by(email=email).count()
        if admin==1:
            raise ValidationError("该邮箱已经被注册！")
    def validate_phone(self,field):
        phone=field.data
        admin=User.query.filter_by(phone=phone).count()
        if admin==1:
            raise ValidationError("该手机号已经被注册！")
class UserLoginForm(FlaskForm):
    name=StringField(
        label='用户名/邮箱/手机号码',
        validators=[
            DataRequired("请输入用户名/邮箱/手机号码'！")
    ],
        description='用户名/邮箱/手机号码',
        render_kw={
                'class':"form-control input-lg",
                'placeholder':"请输入用户名/邮箱/手机号码！",
                'required':'required'
        }
    )
    pwd=PasswordField(
        label='密码',
        validators=[
            DataRequired("请输入密码！")
        ],
        description='密码',
        render_kw={
                'class':"form-control input-lg",
                'placeholder':"请输入密码！",
                'required':'required'
        }
    )
    submit=SubmitField(
        label='登陆',
        render_kw={
            'class':"btn btn-lg btn-success btn-block",
        }

    )
class UserInfoForm(FlaskForm):
    # name=StringField(
    #     label='昵称',
    #     validators=[
    #         DataRequired("请输入昵称'！")
    # ],
    #     description='昵称',
    #     render_kw={
    #             'class':"form-control input-lg",
    #             'placeholder':"请输入昵称！",
    #             'required':'required'
    #     }
    # )
    # email=StringField(
    #     label='邮箱',
    #     validators=[
    #         DataRequired("请输入邮箱'！"),
    #         Email('邮箱格式不正确！')
    # ],
    #     description='邮箱',
    #     render_kw={
    #             'class':"form-control input-lg",
    #             'placeholder':"请输入邮箱！",
    #             'required':'required'
    #     }
    # )
    # phone=StringField(
    #     label='手机号',
    #     validators=[
    #         DataRequired("请输入手机号'！"),
    #         Regexp('1[3458]\\d{9}',message='手机格式不正确！'),
    #         Length(min=11, max=11, message="手机长度不正确！")
    # ],
    #     description='手机号',
    #     render_kw={
    #             'class':"form-control input-lg",
    #             'placeholder':"请输入手机号！",
    #             'required':'required'
    #     }
    # )
    info=StringField(
         label='简介',
         validators=[
                DataRequired("请输入简介！")
            ],
        description='简介',
        render_kw={
                'class':"form-control",
                'rows':5,
                'required':'required'

        })
    submit=SubmitField(
        label='保存修改',
        render_kw={
            'class':"btn btn-success",
        }

    )
class User_Change_pwdForm(FlaskForm):
    old_pwd=PasswordField(
        label='旧密码',
        validators=[
            DataRequired("请输入旧密码！")
        ],
        description='旧密码',
        render_kw={
                'class':"form-control",
                'placeholder':"请输入旧密码！",
                'required':'required'
        }
    )
    new_pwd=PasswordField(
        label='新密码',
        validators=[
            DataRequired("请输入新密码！")
        ],
        description='新密码',
        render_kw={
                'class':"form-control",
                'placeholder':"请输入新密码！",
                'required':'required'
        }
    )
    new_pwd_again=PasswordField(
        label='请再次输入新密码',
        validators=[
            DataRequired("请再次输入新密码！")
        ],
        description='请再次输入新密码',
        render_kw={
                'class':"form-control",
                'placeholder':"请再次输入新密码！",
                'required':'required'
        }
    )
    submit=SubmitField(
        label='修改',
        render_kw={
            # 'class':"btn btn-primary btn-block btn-flat",
            'class':"btn btn-primary",
        }

    )
class AddComment(FlaskForm):
    content=StringField(
        label='评论',
         validators=[
            DataRequired("请输入评论！")
        ],
        description='评论',
        render_kw={
                'class':"form-control input-lg",
        }
    )
    submit=SubmitField(
        label='提交评论',
        render_kw={
            'class':"btn btn-primary",
        })

class AddMoviecol(FlaskForm):
     submit=SubmitField(
        label='收藏电影',
        render_kw={

            'id':'text',
            'class':"btn btn-danger",
        })