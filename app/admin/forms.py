from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, FileField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from .models import Admin, Auth, Role
from app.home.models.movie_models import Tag, Movie


class LoginForm(FlaskForm):
    username = StringField(
        label='用户名',
        validators=[DataRequired('请输入用户名')],
        description='用户名',
        render_kw={
            'class': "form-control",
            'placeholder': "用户名",
        }
    )

    password = PasswordField(
        label='密码',
        validators=[DataRequired('请输入密码')],
        description='密码',
        render_kw={
            'class': "form-control",
            'placeholder': "密码",
        }
    )

    submit = SubmitField(
        '登录',
        render_kw={
            'class': "btn btn-success text-center",
        }
    )

    def validate_username(self, field):
        username = field.data
        admin = Admin.query.filter_by(name=username).first()
        if not admin:
            raise ValidationError('用户名不存在')


class TagForm(FlaskForm):
    tag_name = StringField(
        label='标签名称',
        validators=[DataRequired('请输入标签名称')],
        description='标签名称',
        render_kw={
            'class': 'input-text',
            'placeholder': '请输入标签名称'
        }
    )

    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-success radius'
        }
    )


class MovieForm(FlaskForm):

    def __init__(self):
        super(MovieForm, self).__init__()
        self.tag_id.choices = [(tag.id, tag.name) for tag in Tag.query.all()]

    title = StringField(
        label='视频名称',
        validators=[DataRequired('请输入视频名称')],
        description='视频名称',
        render_kw={'class': 'input-text'}
    )

    star = SelectField(
        label='星级',
        validators=[DataRequired('请选择星级')],
        coerce=int,
        choices=[(1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星')],
        description='星级',
        render_kw={'class': 'select'}
    )

    tag_id = SelectField(
        label='标签',
        validators=[DataRequired('请选择星级')],
        coerce=int,
        choices='',
        description='标签',
        render_kw={'class': 'select'}
    )

    area = StringField(
        label='地区',
        validators=[DataRequired('请输入地区')],
        description='地区',
        render_kw={'class': 'input-text'}
    )

    length = StringField(
        label='时长',
        validators=[DataRequired('请输入时长')],
        description='时长',
        render_kw={'class': 'input-text'}
    )

    release_time = DateField(
        label='上映时间',
        validators=[DataRequired('请输入上映时间')],
        description='上映时间',
        render_kw={
            'onfocus': "WdatePicker({dateFmt:'yyyy-MM-dd'})",
            'class': 'input-text Wdate'
        }
    )

    logo = FileField(
        label='封面',
        validators=[DataRequired('请选择封面')],
        description='封面',
        render_kw={
            'class': 'input-file'
        }
    )

    url = FileField(
        label='视频',
        validators=[DataRequired('请选择视频')],
        description='视频',
        render_kw={'class': 'input-file'}
    )

    info = TextAreaField(
        label='简介',
        validators=[DataRequired('请输入简介')],
        description='简介',
        render_kw={
            'class': 'textarea',
            'onKeyUp': "textarealength(this,100)",
            'placeholder': '请输入最少10个字符'
        }
    )

    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-success radius'
        }
    )


class BannerForm(FlaskForm):

    def __init__(self):
        super().__init__()
        self.movie_id.choices = [(movie.id, movie.title) for movie in Movie.query.all()]

    movie_id = SelectField(
        validators=[DataRequired('请选择电影')],
        coerce=int,
        choices='',
        description='电影',
        render_kw={'class': 'select'}
    )

    logo = FileField(
        label='轮播图封面',
        validators=[DataRequired('请输入轮播图封面')],
        description='轮播图封面',
        render_kw={'class': 'input-file'}
    )

    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-success radius'
        }
    )


class PasswordForm(FlaskForm):
    old_pwd = PasswordField(
        label='旧密码',
        validators=[DataRequired('请输入旧密码')],
        description='旧密码',
        render_kw={
            'class': "input-text",
            'placeholder': "旧密码",
        }
    )

    password1 = PasswordField(
        label='新密码',
        validators=[DataRequired('请输入新密码')],
        description='新密码',
        render_kw={
            'class': "input-text",
            'placeholder': "新密码",
        }
    )

    password2 = PasswordField(
        label='确认密码',
        validators=[DataRequired('请输入新密码'), EqualTo('password1', '两次密码不一致')],
        description='确认密码',
        render_kw={
            'class': "input-text",
            'placeholder': "确认密码",
        }
    )

    submit = SubmitField(
        '确认',
        render_kw={
            'class': 'btn btn-success radius'
        }
    )

    def validate_old_pwd(self, field):
        from flask import session
        old_pwd = field.data
        admin = Admin.query.filter_by(name=session['admin']).first()
        if not admin.check_pwd(old_pwd):
            raise ValidationError('旧密码错误')


class AuthForm(FlaskForm):
    name = StringField(
        label='权限名称',
        validators=[DataRequired('请输入权限名称')],
        description='权限名称',
        render_kw={
            'class': 'input-text',
        }
    )

    url = StringField(
        label='权限地址',
        validators=[DataRequired('请输入权限地址')],
        description='权限地址',
        render_kw={
            'class': 'input-text',
        }
    )

    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-success radius'
        }
    )


class RoleForm(FlaskForm):
    def __init__(self):
        super().__init__()
        self.auths.choices = [(auth.id, auth.name) for auth in Auth.query.all()]

    name = StringField(
        label='角色名称',
        validators=[DataRequired('请输入角色名称')],
        description='角色名称',
        render_kw={
            'class': 'input-text',
        }
    )

    auths = SelectMultipleField(
        label='权限列表',
        validators=[DataRequired('请输入权限名称')],
        description='权限名称',
        coerce=int,
        choices='',
        render_kw={
            'class': 'select',
        }
    )

    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-success radius'
        }
    )


class AdminForm(FlaskForm):
    def __init__(self):
        super(AdminForm, self).__init__()
        self.role_id.choices = [(role.id, role.name) for role in Role.query.all()]

    name = StringField(
        label='管理员名称',
        validators=[DataRequired('请输入管理员名称')],
        description='管理员名称',
        render_kw={
            'class': "input-text",
        }
    )

    password1 = PasswordField(
        label='密码',
        validators=[DataRequired('请输入密码')],
        description='密码',
        render_kw={
            'class': "input-text",
        }
    )

    password2 = PasswordField(
        label='确认密码',
        validators=[DataRequired('请输入新密码'), EqualTo('password1', '两次密码不一致')],
        description='确认密码',
        render_kw={
            'class': "input-text",
        }
    )

    role_id = SelectField(
        label='所属角色',
        coerce=int,
        choices=[],
        render_kw={'class': 'select'}
    )

    submit = SubmitField(
        '确认',
        render_kw={
            'class': 'btn btn-success radius'
        }
    )

