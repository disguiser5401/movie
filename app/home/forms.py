from flask_wtf import FlaskForm
from flask import session
from wtforms import StringField, PasswordField, SubmitField, ValidationError, FileField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp
from .models.user_models import User


class LoginForm(FlaskForm):
    username = StringField(
        label='账号',
        validators=[DataRequired('请输入账号')],
        description='账号',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入账号",
        }
    )

    password = PasswordField(
        label='密码',
        validators=[DataRequired('请输入密码')],
        description='密码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入密码",
        }
    )

    submit = SubmitField(
        '登录',
        render_kw={
            'class': "btn btn-lg btn-danger btn-block",
        }
    )

    def validate_username(self, field):
        username = field.data
        if not User.query.filter_by(name=username).first():
            raise ValidationError('用户名不存在')


class RegisterForm(FlaskForm):
    name = StringField(
        validators=[
            DataRequired('请输入昵称')
        ],
        description='昵称',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入昵称'
        }
    )

    email = StringField(
        validators=[
            DataRequired('请输入邮箱'),
            Email('邮箱格式不正确')
        ],
        description='邮箱',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入邮箱'
        }
    )

    phone = StringField(
        validators=[
            DataRequired('请输入手机'),
            Regexp(r'1[3458]\d{9}', message='手机格式不正确')
        ],
        description='手机',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入手机'
        }
    )

    password1 = PasswordField(
        validators=[DataRequired('请输入密码')],
        description='密码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入密码",
        }
    )

    password2 = PasswordField(
        validators=[DataRequired('请输入密码'), EqualTo('password1', '两次密码不一致')],
        description='确认密码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "确认密码",
        }
    )

    submit = SubmitField(
        '注册',
        render_kw={
            'class': 'btn btn-lg btn-success btn-block'
        }
    )

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    def validate_phone(self, field):
        if User.query.filter_by(phone=field.data).first():
            raise ValidationError('手机已被注册')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('昵称已被注册')


class UserForm(FlaskForm):
    def __init__(self):
        self._user = User.query.get(session['user_id'])
        super(UserForm, self).__init__()

    name = StringField(
        validators=[
            DataRequired('请输入昵称')
        ],
        description='昵称',
        render_kw={
            'class': 'layui-input',
            'placeholder': '请输入昵称',
            'lay-verify': "required",

        }
    )

    email = StringField(
        validators=[
            DataRequired('请输入邮箱'),
            Email('邮箱格式不正确')
        ],
        description='邮箱',
        render_kw={
            'class': 'layui-input',
            'placeholder': '请输入邮箱',
            'lay-verify': "required"
        }
    )

    phone = StringField(
        validators=[
            DataRequired('请输入手机'),
            Regexp(r'1[3458]\d{9}', message='手机格式不正确')
        ],
        description='手机',
        render_kw={
            'class': 'layui-input',
            'placeholder': '请输入手机',
            'lay-verify': "required"
        }
    )

    face = FileField(
        description='头像',
        render_kw={'class': 'hidden'}
    )

    info = TextAreaField(
        validators=[DataRequired('请输入简介')],
        description='简介',
        render_kw={
            'class': 'layui-textarea',
            'lay-verify': "required",
            'placeholder': '请输入简介'
        }
    )

    submit = SubmitField(
        '确认修改',
        render_kw={
            'class': 'layui-btn layui-btn-normal',
            'lay-submit': ''
        }
    )

    def validate_name(self, filed):
        if User.query.filter_by(name=filed.data).first() and self._user.name != filed.data:
            raise ValueError('用户名已存在')

    def validate_email(self, filed):
        if User.query.filter_by(email=filed.data).first() and self._user.email != filed.data:
            raise ValueError('邮箱已存在')

    def validate_phone(self, filed):
        if User.query.filter_by(phone=filed.data).first() and self._user.phone != filed.data:
            raise ValueError('手机号已存在')


class PasswordForm(FlaskForm):
    old_pwd = PasswordField(
        label='旧密码',
        validators=[DataRequired('请输入旧密码')],
        description='旧密码',
        render_kw={
            'class': "layui-input",
            'placeholder': "请输入旧密码",
            'lay-verify': "required",
        }
    )

    password1 = PasswordField(
        label='新密码',
        validators=[DataRequired('请输入新密码')],
        description='新密码',
        render_kw={
            'class': "layui-input",
            'placeholder': "请输入新密码",
            'lay-verify': "required",
        }
    )

    password2 = PasswordField(
        label='确认密码',
        validators=[DataRequired('请输入新密码'), EqualTo('password1', '两次密码不一致')],
        description='确认密码',
        render_kw={
            'class': "layui-input",
            'placeholder': "确认密码",
            'lay-verify': "required",
        }
    )

    submit = SubmitField(
        '确认修改',
        render_kw={
            'class': 'layui-btn layui-btn-normal',
            'lay-submit': ''
        }
    )

    def validate_old_pwd(self, field):
        old_pwd = field.data
        user = User.query.get(session['user_id'])
        if not user.check_pwd(old_pwd):
            raise ValidationError('旧密码错误')


class CommentForm(FlaskForm):
    input_content = TextAreaField(
        label='评论',
        validators=[DataRequired('请输入评论内容')],
        description='评论内容',
        render_kw={'class': 'hidden'}
    )

    submit = SubmitField(
        '发表评论',
        render_kw={
            'class': 'layui-btn pull-right',
        }
    )
