#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/5/16
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,FileField,TextAreaField,SelectField,DateTimeField,IntegerField,SelectMultipleField
from wtforms.validators import DataRequired,ValidationError,EqualTo
from myapp.models import Admin,Tag,Movie,Auth,Role

tags=Tag.query.all()
auths_list=Auth.query.all()
role_list=Role.query.all()
#管理员登陆表单
class LoginForm(FlaskForm):
    account=StringField(
        label='账号',
        validators=[
            DataRequired("请输入账号！")
    ],
        description='账号',
        render_kw={
                'class':"form-control",
                'placeholder':"请输入账号！",
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
                'class':"form-control",
                'placeholder':"请输入密码！",
                'required':'required'
        }
    )
    submit=SubmitField(
        label='登陆',
        render_kw={
            'class':"btn btn-primary btn-block btn-flat",
        }

    )
    def validate_account(self,field):
        account=field.data
        admin=Admin.query.filter_by(name=account).count()
        if admin==0:
            raise ValidationError("该账号不存在！")

class MovieForm(FlaskForm):
     # id=IntegerField(
     #    label='编号',
     #    validators=[
     #        DataRequired('请输入编号！')
     #
     #    ],
     #    description='编号',
     #    render_kw={
     #        'class':"form-control",
     #        'id':"input_name" ,
     #        'placeholder':"请输入编号名称！",
     #        'required':'required'
     #    }
     # )
     title=StringField(
        label='片名',
        validators=[
            DataRequired("请输入片名！")
        ],
        description='片名',
        render_kw={
                'class':"form-control",
                'id':'input_title',
                'placeholder':"请输入片名！",'required':'required'

        })
     url=FileField(
         label='电影文件',
         validators=[
                DataRequired("请上传文件！")
            ],
        description='片名',)
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
     logo=FileField(
         label='封面',
         validators=[
                DataRequired("请上传封面！")
            ],
        description='封面',
        render_kw={
                    'width':'100px',
                    'height':'100px',
             }
     )
     star=SelectField(
         label='星级',
         validators=[
                DataRequired("请选择星级！")
            ],
         coerce=int,
         choices=[(1,'1⭐'),(2,'2⭐'),(3,'3⭐'),(4,'4⭐'),(5,'5⭐')],
         description='星级',
         render_kw={
                'class':"form-control",
                'required':'required'
         }
     )

     tag_id=SelectField(
     label='标签',
     validators=[
            DataRequired("请选择标签！")
        ],
     coerce=int,
     choices=[(v.id,v.name) for v in tags],
     description='星级',
     render_kw={
            'class':"form-control",
     })
     area=StringField(
        label='地区',
        validators=[
            DataRequired("请输入地区！")
        ],
        description='地区',
        render_kw={
                'class':"form-control",
                'placeholder':"请输入地区！",

        })
     length=StringField(
     label='片长',
     validators=[
        DataRequired("请输入片长！")
     ],
     description='片长',
     render_kw={
            'class':"form-control",
            'placeholder':"请输入片长！",

     })
     releasetime=StringField(
         label='上映时间',
         validators=[
            DataRequired("请选择上映时间！")
         ],
         description='上映时间',
         render_kw={
                'class':"form-control",
                'placeholder':"请选择上映时间！",
                'id':'input_release_time'

         })
     submit=SubmitField(
        label='编辑',
        render_kw={
            'class':"btn btn-primary btn-block btn-flat",
        }

    )
class TagForm(FlaskForm):
    # id=IntegerField(
    #     label='编号',
    #     # validators=[
    #     #     DataRequired('请输入编号！')
    #     #
    #     # ],
    #     description='编号',
    #     render_kw={
    #         'class':"form-control",
    #         'id':"input_name" ,
    #         'placeholder':"请输入编号名称！"
    #     }
    # )
    name=StringField(
        label='名称',
        validators=[
            DataRequired('请输入标签！')

        ],
        description='标签',
        render_kw={
            'class':"form-control",
            'id':"input_name" ,
            'placeholder':"请输入标签名称！"
        }
    )
    submit=SubmitField(
        label='编辑',
        render_kw={

            'class':"btn btn-primary"
        }
    )

class UserForm(FlaskForm):
    name=StringField(
        label='昵称',
        validators=[
            DataRequired('请输入昵称！')

        ],
        description='昵称',
        render_kw={
            'class':"form-control",
            'id':"input_name" ,
            'placeholder':"请输入昵称！"
        }
    )
    email=StringField(
        label='邮箱',
        validators=[
            DataRequired('请输入邮箱！')

        ],
        description='邮箱',
        render_kw={
            'class':"form-control",
            'id':"input_name" ,
            'placeholder':"请输入邮箱！"
        }
    )
    phone=StringField(
        label='联系方式',
        validators=[
            DataRequired('请输入联系方式！')

        ],
        description='联系方式',
        render_kw={
            'class':"form-control",
            'id':"input_name" ,
            'placeholder':"请输入联系方式！"
        }
    )

    face=FileField(
         label='头像',
         validators=[
                DataRequired("请上传头像！")
            ],
        description='头像',)
    status=SelectField(
     label='状态',
     validators=[
            DataRequired("请选择状态！")
        ],
     choices=[('1','正常'),('2','冻结')],
     description='状态',
     render_kw={
            'class':"form-control",
     })
    addtime=StringField(
         label='注册时间',
         validators=[
            DataRequired("请选择注册时间！")
         ],
         description='注册时间',
         render_kw={
                'class':"form-control",
                'placeholder':"请选择注册时间！",
                'id':'input_release_time'

         })
    uuid=StringField(
        label='唯一标识符',
         validators=[
            DataRequired("请输入唯一标识符！")
         ],
         description='唯一标识符',
         render_kw={
                'class':"form-control",
                'placeholder':"请输入唯一标识符！",
                'id':'input_release_time'

         })
    info=TextAreaField(
         label='个性简介',
         validators=[
            DataRequired("请输入个性简介！")
         ],
         description='个性简介',
         render_kw={
                'class':"form-control",
                'placeholder':"请输入个性简介！",
                'id':'input_release_time'

         })
    # submit=SubmitField(
    #     label='编辑',
    #     render_kw={
    #
    #         'class':"btn btn-primary btn-block btn-flat"
    #     }
    # )


class PreviewForm(FlaskForm):
     title=StringField(
        label='预告标题',
        validators=[
            DataRequired("请输入预告标题！")
        ],
        description='预告标题',
        render_kw={
                'class':"form-control",
                'id':'input_title',
                'placeholder':"请输入预告标题！",
                'required':'required'

        })
     url=FileField(
         label='预告封面',
         validators=[
                DataRequired("请上传预告封面！")
            ],
        description='预告封面',)

     submit=SubmitField(
        label='编辑',
        render_kw={

            'class':"btn btn-primary btn-block btn-flat"
        }
     )
class Change_pwdForm(FlaskForm):
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
class AuthForm(FlaskForm):
    name=StringField(
        label='权限名称',
        validators=[
            DataRequired("请输入权限名称！")
        ],
        description='权限名称',
        render_kw={
                'class':"form-control",
                'id':'input_title',
                'placeholder':"请输入权限名称！",
                'required':'required'

        })
    url=StringField(
        label='权限地址',
        validators=[
            DataRequired("请输入权限地址！")
        ],
        description='权限地址',
        render_kw={
                'class':"form-control",
                'id':'input_title',
                'placeholder':"请输入权限地址！",
                'required':'required'

        })

    submit=SubmitField(
        label='编辑',
        render_kw={

            'class':"btn btn-primary"
        }
     )
class RoleForm(FlaskForm):
     name=StringField(
        label='角色名称',
        validators=[
            DataRequired("请输入角色名称！")
        ],
        description='角色名称',
        render_kw={
                'class':"form-control",
                'id':'input_title',
                'placeholder':"请输入角色名称！",
                'required':'required'

        })
     auths=SelectMultipleField(
         label='权限列表',
         validators=[
            DataRequired("请选择权限列表！")
        ],
        coerce=int,
        choices=[(v.id  ,v.name) for v in auths_list],
        description='权限列表',
        render_kw={
                'class':"form-control",
                'id':'input_title',
                'placeholder':"请选择权限名称！",
                'required':'required'

        })
     submit=SubmitField(
        label='编辑',
        render_kw={

            'class':"btn btn-primary"
        }
     )


class AdminForm(FlaskForm):
     name=StringField(
        label='管理员名称',
        validators=[
            DataRequired("请输入管理员名称！")
        ],
        description='管理员名称',
        render_kw={
                'class':"form-control",
                'id':'input_title',
                'placeholder':"请输入管理员名称！",
                'required':'required'

        })
     pwd=PasswordField(
        label='管理员密码',
        validators=[
            DataRequired("请输入管理员密码！")
        ],
        description='管理员密码',
        render_kw={
                'class':"form-control",
                'placeholder':"请输入管理员密码！",
                'required':'required'
        }
    )
     pwd_again=PasswordField(
        label='管理员重复密码',
        validators=[
            DataRequired("请输入管理员重复密码！"),
            # EqualTo(pwd,message='两次输入的密码不一致！')
        ],
        description='请输入管理员重复密码',
        render_kw={
                'class':"form-control",
                'placeholder':"请输入管理员重复密码！",
                'required':'required',
        }
    )
     role=SelectField(
         label='所属角色',
          validators=[
            DataRequired("请选择所属角色！")
        ],
        coerce=int,
        choices=[(v.id,v.name) for v in role_list],
        description='所属角色',
        render_kw={
                'class':"form-control"

        })
     submit=SubmitField(
        label='添加',
        render_kw={
            # 'class':"btn btn-primary btn-block btn-flat",
            'class':"btn btn-primary",
        }

    )