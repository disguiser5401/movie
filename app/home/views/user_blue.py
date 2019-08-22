from flask import render_template, Blueprint, redirect, url_for, flash, session, request, current_app
from app.extensions import db
from app.home.forms import LoginForm, RegisterForm, UserForm, PasswordForm
from app.home.models.user_models import User, UserLog
from app.home.models.operation_models import Collection, Comment, Score
from functools import wraps
from app.extensions import change_filename
from werkzeug.security import generate_password_hash

blue_user = Blueprint('blue_user', __name__, url_prefix='/user')


def user_login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('blue_user.login', next=request.url))
        return func(*args, **kwargs)
    return inner


@blue_user.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.data['username']).first()
        if not user.check_pwd(form.data['password']):
            flash('密码错误', 'pwd_err')
            return render_template('home/login.html', form=form)
        session['user'] = user.name
        session['user_id'] = user.id
        _log = UserLog(user_id=user.id, ip=request.remote_addr)
        db.session.add(_log)
        db.session.commit()
        return redirect(request.args.get('next') or url_for('blue_index.index'))
    return render_template('home/login.html', form=form)


@blue_user.route('/logout/')
@user_login_required
def logout():
    session.pop('user')
    session.pop('user_id')
    return redirect(url_for('blue_user.login'))


@blue_user.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.data['name'],
            phone=form.data['phone'],
            email=form.data['email'],
            pwd=generate_password_hash(form.data['password1'])
        )
        db.session.add(user)
        _log = UserLog(user_id=user.id, ip=request.remote_addr)
        db.session.add(_log)
        db.session.commit()
        session['user'] = user.name
        session['user_id'] = user.id
        return redirect(url_for('blue_index.index'))
    return render_template('home/register.html', form=form)


@blue_user.route('/info/', methods=['GET', 'POST'])
@user_login_required
def user_info():
    form = UserForm()
    user = User.query.get(session['user_id'])
    if request.method == 'GET':
        form.info.data = user.info
    if form.validate_on_submit():
        if form.face.data != '':
            file_face = form.face.data.filename
            face = change_filename(file_face)
            form.face.data.save(current_app.config['MEDIA_DIR'] + 'user/' + face)
            user.face = face
        user.name = form.data['name']
        user.email = form.data['email']
        user.phone = form.data['phone']
        user.info = form.data['info']
        db.session.add(user)
        db.session.commit()
        flash('信息修改成功')
        return redirect(url_for('blue_user.user_info'))
    return render_template('home/user_info.html', form=form, user=user)


@blue_user.route('/pwd/', methods=['GET', 'POST'])
@user_login_required
def pwd():
    form = PasswordForm()
    if form.validate_on_submit():
        user = User.query.get(session['user_id'])
        user.pwd = generate_password_hash(form.data['password1'])
        db.session.add(user)
        db.session.commit()
        flash('密码修改成功', 'change_pwd_success')
        return redirect(url_for('blue_user.logout'))
    return render_template('home/pwd.html', form=form)


@blue_user.route('/comment/<int:page>/')
@user_login_required
def comment(page):
    page_data = Comment.query.filter_by(user_id=session['user_id']).paginate(page=page, per_page=10)
    return render_template('home/comment.html', page_data=page_data)


@blue_user.route('/log/<int:page>/')
@user_login_required
def log(page):
    page_data = UserLog.query.filter_by(user_id=session['user_id']).paginate(page=page, per_page=10)
    return render_template('home/log.html', page_data=page_data)


@blue_user.route('/collection/<int:page>/')
@user_login_required
def collection(page):
    page_data = Collection.query.filter_by(user_id=session['user_id']).paginate(page=page, per_page=10)
    return render_template('home/collection.html', page_data=page_data)


@blue_user.route('/score/<int:page>/')
@user_login_required
def score(page):
    page_data = Score.query.filter_by(user_id=session['user_id']).paginate(page=page, per_page=10)
    return render_template('home/score.html', page_data=page_data)
