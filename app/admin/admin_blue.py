from flask import render_template, Blueprint, redirect, url_for, flash, session, request, jsonify, current_app, abort
from app.extensions import db, change_filename
from .forms import LoginForm, TagForm, MovieForm, BannerForm, PasswordForm, AuthForm, RoleForm, AdminForm
from .models import Admin, Role, OperationLog, AdminLog, Auth
from app.home.models.movie_models import Tag, Movie, Banner
from app.home.models.user_models import User, UserLog
from app.home.models.operation_models import Comment, Collection
from sqlalchemy import or_
from functools import wraps
from werkzeug.security import generate_password_hash
blue_admin = Blueprint('blue_admin', __name__, url_prefix='/admin')


def admin_login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('blue_admin.login', next=request.url))
        return func(*args, **kwargs)
    return inner


def auth_admin(func):
    @wraps(func)
    def inner(*args, **kwargs):
        admin = Admin.query.get_or_404(session['admin_id'])
        if not admin.is_super:
            url_list = [auth.url for auth in Auth.query.filter(Auth.id.in_(admin.role.auth_list.split(','))).all()]
            if str(request.url_rule) not in url_list:
                abort(403)
        return func(*args, **kwargs)
    return inner


@blue_admin.route('/')
@admin_login_required
def index():
    return render_template('admin/index.html')


@blue_admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data['username']).first()
        if not admin.check_pwd(data['password']):
            flash('密码错误')
            return redirect(url_for('blue_admin.login'))
        session['admin'] = data['username']
        session['admin_id'] = admin.id
        log = AdminLog(admin_id=admin.id, ip=request.remote_addr)
        db.session.add(log)
        db.session.commit()
        return redirect(request.args.get('next') or url_for('blue_admin.index'))
    return render_template('admin/login.html', form=form)


@blue_admin.route('/logout/')
@admin_login_required
def logout():
    session.pop('admin')
    session.pop('admin_id')
    return redirect(url_for('blue_admin.login'))


@blue_admin.route('/change_pwd/', methods=['GET', 'POST'])
@admin_login_required
def change_pwd():
    form = PasswordForm()
    if form.validate_on_submit():
        password1 = form.data['password1']
        admin = Admin.query.filter_by(name=session['admin']).first()
        admin.pwd = generate_password_hash(password1)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('blue_admin.logout'))
    return render_template('admin/change_pwd.html', form=form)


@blue_admin.route('/tag/list/')
@admin_login_required
@auth_admin
def tag_list():
    tags = Tag.query.all()
    return render_template('admin/tag_list.html', tags=tags)


@blue_admin.route('/tag/add/', methods=['GET', 'POST'])
@admin_login_required
@auth_admin
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        tag_name = form.data['tag_name']
        if Tag.query.filter_by(name=tag_name).first():
            flash('标签已存在')
            return redirect(url_for('blue_admin.tag_add'))
        tag = Tag(name=tag_name)
        op_log = OperationLog(admin_id=session['admin_id'], ip=request.remote_addr, reason='添加标签:{}'.format(tag_name))
        db.session.add(tag)
        db.session.add(op_log)
        db.session.commit()
        return render_template('admin/add_success.html')
    return render_template('admin/tag_add.html', form=form)


@blue_admin.route('/tag/edit/<int:tag_id>/', methods=['GET', 'POST'])
@admin_login_required
@auth_admin
def tag_edit(tag_id):
    form = TagForm()
    tag = Tag.query.get_or_404(tag_id)
    if request.method == 'GET':
        return render_template('admin/tag_edit.html', form=form, tag=tag)
    else:
        if form.validate_on_submit():
            tag_name = form.data['tag_name']
            if Tag.query.filter_by(name=tag_name).first() and tag.name != tag_name:
                flash('标签名已存在')
                return redirect(url_for('blue_admin.tag_edit', tag_id=tag.id))
            tag.name = tag_name
            db.session.add(tag)
            db.session.commit()
            return render_template('admin/add_success.html')


@blue_admin.route('/tag/del/', methods=['POST'])
@admin_login_required
@auth_admin
def tag_del():
    tags = request.form.getlist('id_list', None)
    Tag.query.filter(Tag.id.in_(tags)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({'status': 'ok'})


@blue_admin.route('/movie/list/')
@admin_login_required
@auth_admin
def movie_list():
    movies = Movie.query.all()
    return render_template('admin/movie_list.html', movies=movies)


@blue_admin.route('/movie/add/', methods=['GET', 'POST'])
@admin_login_required
@auth_admin
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        file_url = form.url.data.filename
        file_logo = form.logo.data.filename
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(current_app.config['MEDIA_DIR'] + 'movie_url/' + url)
        form.logo.data.save(current_app.config['MEDIA_DIR'] + 'movie_logo/' + logo)
        movie = Movie(
            title=data['title'],
            url=url,
            info=data['info'],
            logo=logo,
            star=data['star'],
            tag_id=data['tag_id'],
            area=data['area'],
            release_time=data['release_time'],
            length=data['length']
        )
        db.session.add(movie)
        db.session.commit()
        return render_template('admin/add_success.html')
    return render_template('admin/movie_add.html', form=form)


@blue_admin.route('/movie/edit/<int:movie_id>/', methods=['GET', 'POST'])
@admin_login_required
@auth_admin
def movie_edit(movie_id):
    form = MovieForm()
    movie = Movie.query.get_or_404(movie_id)
    form.url.validators = []
    form.logo.validators = []
    if request.method == 'GET':
        form.star.data = movie.star
        form.tag_id.data = movie.tag_id
        form.info.data = movie.info
        return render_template('admin/movie_edit.html', form=form, movie=movie)
    else:
        if form.validate_on_submit():
            movie_title = form.data['title']
            if Movie.query.filter_by(title=movie_title).first() and movie.title != movie_title:
                flash('片名已存在')
                return redirect(url_for('blue_admin.movie_edit', movie_id=movie.id))
            if form.url.data != '':
                file_url = form.url.data.filename
                url = change_filename(file_url)
                form.url.data.save(current_app.config['MEDIA_DIR'] + 'movie_url/' + url)
                movie.url = url
            if form.logo.data != '':
                file_logo = form.logo.data.filename
                logo = change_filename(file_logo)
                form.logo.data.save(current_app.config['MEDIA_DIR'] + 'movie_logo/' + logo)
                movie.logo = logo
            movie.title = form.data['title'],
            movie.info = form.data['info'],
            movie.star = form.data['star'],
            movie.tag_id = form.data['tag_id'],
            movie.area = form.data['area'],
            movie.release_time = form.data['release_time'],
            movie.length = form.data['length']
            db.session.add(movie)
            db.session.commit()
            return render_template('admin/add_success.html')


@blue_admin.route('/movie/del/', methods=['POST'])
@admin_login_required
@auth_admin
def movie_del():
    movies = request.form.getlist('id_list', None)
    Movie.query.filter(Movie.id.in_(movies)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({'status': 'ok'})


@blue_admin.route('/banner/list/')
@admin_login_required
@auth_admin
def banner_list():
    banners = Banner.query.all()
    return render_template('admin/banner_list.html', banners=banners)


@blue_admin.route('/banner/add/', methods=['GET', 'POST'])
@admin_login_required
@auth_admin
def banner_add():
    form = BannerForm()
    if form.validate_on_submit():
        movie_id = form.data['movie_id']
        if Banner.query.filter_by(movie_id=movie_id).first():
            flash('轮播图已存在')
            return redirect(url_for('blue_admin.banner_add'))
        file_logo = form.logo.data.filename
        logo = change_filename(file_logo)
        form.logo.data.save(current_app.config['MEDIA_DIR'] + 'banner_logo/' + logo)
        banner = Banner(logo=logo, movie_id=movie_id)
        db.session.add(banner)
        db.session.commit()
        return render_template('admin/add_success.html')
    return render_template('admin/banner_add.html', form=form)


@blue_admin.route('/banner/edit/<int:banner_id>/', methods=['GET', 'POST'])
@admin_login_required
@auth_admin
def banner_edit(banner_id):
    form = BannerForm()
    banner = Banner.query.get_or_404(banner_id)
    form.logo.validators = []
    if request.method == 'GET':
        form.movie_id.data = banner.movie_id
        return render_template('admin/banner_edit.html', form=form, banner=banner)
    else:
        if form.validate_on_submit():
            movie_id = form.data['movie_id']
            if Banner.query.filter_by(movie_id=movie_id).first() and banner.movie_id != movie_id:
                flash('轮播图已存在')
                return redirect(url_for('blue_admin.banner_edit', banner_id=banner.id))
            if form.logo.data != '':
                file_logo = form.logo.data.filename
                logo = change_filename(file_logo)
                form.logo.data.save(current_app.config['MEDIA_DIR'] + 'banner_logo/' + logo)
                banner.logo = logo
            banner.movie_id = form.data['movie_id'],
            db.session.add(banner)
            db.session.commit()
    return render_template('admin/add_success.html')


@blue_admin.route('/banner/del/', methods=['POST'])
@admin_login_required
@auth_admin
def banner_del():
    banners = request.form.getlist('id_list', None)
    Banner.query.filter(Banner.id.in_(banners)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({'status': 'ok'})


@blue_admin.route('/member/list/')
@admin_login_required
@auth_admin
def member_list():
    users = User.query.all()
    return render_template('admin/member_list.html', users=users)


@blue_admin.route('/member/del/', methods=['POST'])
@admin_login_required
@auth_admin
def member_del():
    users = request.form.getlist('id_list', None)
    User.query.filter(User.id.in_(users)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({'status': 'ok'})


@blue_admin.route('/comment/list/')
@admin_login_required
@auth_admin
def comment_list():
    comments = Comment.query.all()
    return render_template('admin/comment_list.html', comments=comments)


@blue_admin.route('/comment/del/', methods=['POST'])
@admin_login_required
@auth_admin
def comment_del():
    comments = request.form.getlist('id_list', None)
    Comment.query.filter(Comment.id.in_(comments)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({'status': 'ok'})


@blue_admin.route('/collect/list/')
@admin_login_required
@auth_admin
def collect_list():
    collections = Collection.query.all()
    return render_template('admin/collect_list.html', collections=collections)


@blue_admin.route('/collection/del/', methods=['POST'])
@admin_login_required
@auth_admin
def collection_del():
    collections = request.form.getlist('id_list', None)
    Collection.query.filter(Collection.id.in_(collections)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({'status': 'ok'})


@blue_admin.route('/operation_log/')
@admin_login_required
@auth_admin
def operation_log():
    op_logs = OperationLog.query.all()
    return render_template('admin/operation_log.html', op_logs=op_logs)


@blue_admin.route('/admin_log/')
@admin_login_required
@auth_admin
def admin_log():
    logs = AdminLog.query.all()
    return render_template('admin/admin_log.html', logs=logs)


@blue_admin.route('/user_log/')
@admin_login_required
@auth_admin
def user_log():
    logs = UserLog.query.all()
    return render_template('admin/user_log.html', logs=logs)


@blue_admin.route('/auth/list/')
@admin_login_required
@auth_admin
def auth_list():
    auths = Auth.query.all()
    return render_template('admin/auth_list.html', auths=auths)


@blue_admin.route('/auth/add/', methods=['GET', 'POST'])
@admin_login_required
@auth_admin
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        auth_name = form.data['name']
        auth_url = form.data['url']
        if Auth.query.filter(or_(Auth.name == auth_name, Auth.url == auth_url)).first():
            flash('权限已存在')
            return redirect(url_for('blue_admin.auth_add'))
        auth = Auth(name=auth_name, url=auth_url)
        db.session.add(auth)
        db.session.commit()
        return render_template('admin/add_success.html')
    return render_template('admin/auth_add.html', form=form)


@blue_admin.route('/auth/edit/<int:auth_id>/', methods=['GET', 'POST'])
@admin_login_required
@auth_admin
def auth_edit(auth_id):
    form = AuthForm()
    auth = Auth.query.get_or_404(auth_id)
    if request.method == 'GET':
        return render_template('admin/auth_edit.html', form=form, auth=auth)
    else:
        if form.validate_on_submit():
            auth_name = form.data['name']
            auth_url = form.data['url']
            name_count = Auth.query.filter_by(name=auth_name).count()
            url_count = Auth.query.filter_by(url=auth_url).count()
            if (name_count and auth.name != auth_name) or (url_count and auth.url != auth_url):
                flash('权限已存在')
                return redirect(url_for('blue_admin.auth_edit', auth_id=auth.id))
            auth.name = auth_name
            auth.url = auth_url
            db.session.add(auth)
            db.session.commit()
            return render_template('admin/add_success.html')


@blue_admin.route('/auth/del/', methods=['POST'])
@admin_login_required
@auth_admin
def auth_del():
    auths = request.form.getlist('id_list', None)
    Auth.query.filter(Auth.id.in_(auths)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({'status': 'ok'})


@blue_admin.route('/role/list/')
@admin_login_required
@auth_admin
def role_list():
    roles = Role.query.all()
    return render_template('admin/role_list.html', roles=roles)


@blue_admin.route('/role/add/', methods=['GET', 'POST'])
@admin_login_required
@auth_admin
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        role_name = form.data['name']
        if Role.query.filter_by(name=role_name).first():
            flash('角色名称已存在')
            return redirect(url_for('blue_admin.role_add'))
        role = Role(name=form.data['name'], auth_list=','.join(map(lambda i: str(i), form.data['auths'])))
        db.session.add(role)
        db.session.commit()
        return render_template('admin/add_success.html')
    return render_template('admin/role_add.html', form=form)


@blue_admin.route('/role/edit/<int:role_id>/', methods=['GET', 'POST'])
@admin_login_required
@auth_admin
def role_edit(role_id):
    form = RoleForm()
    role = Role.query.get_or_404(role_id)
    if request.method == 'GET':
        form.auths.data = [int(i) for i in role.auth_list.split(',')]
        return render_template('admin/role_edit.html', form=form, role=role)
    else:
        if form.validate_on_submit():
            role_name = form.data['name']
            if Role.query.filter_by(name=role_name).first() and role.name != role_name:
                flash('角色名称已存在')
                return redirect(url_for('blue_admin.role_edit', role_id=role.id))
            role.name = role_name
            role.auth_list = ','.join(map(lambda i: str(i), form.data['auths']))
            db.session.add(role)
            db.session.commit()
            return render_template('admin/add_success.html')


@blue_admin.route('/role/del/', methods=['POST'])
@admin_login_required
@auth_admin
def role_del():
    roles = request.form.getlist('id_list', None)
    Role.query.filter(Role.id.in_(roles)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({'status': 'ok'})


@blue_admin.route('/admin/list')
@admin_login_required
@auth_admin
def admin_list():
    admins = Admin.query.all()
    return render_template('admin/admin_list.html', admins=admins)


@blue_admin.route('/admin/add/', methods=['GET', 'POST'])
@admin_login_required
@auth_admin
def admin_add():
    form = AdminForm()
    if form.validate_on_submit():
        admin_name = form.data['name']
        if Admin.query.filter_by(name=admin_name).first():
            flash('管理员名称已存在')
            return redirect(url_for('blue_admin.admin_add'))
        admin = Admin(name=admin_name, pwd=generate_password_hash(form.data['password1']), is_super=False, role_id=form.data['role_id'])
        db.session.add(admin)
        db.session.commit()
        return render_template('admin/add_success.html')
    return render_template('admin/admin_add.html', form=form)


def createsuperuser():
    role = Role.query.filter_by(name='超级管理员').first()
    if not role:
        role = Role(name='超级管理员', auth_list='')
        db.session.add(role)
    while True:
        name = input('请输入管理员账号:')
        if Admin.query.filter_by(name=name).first():
            print('账号已存在！')
            continue
        pwd = input('请输入管理员密码:')
        pwd1 = input('请确认管理员密码:')
        if not all([pwd, pwd1]):
            print('密码不能为空！')
        if pwd != pwd1:
            print('两次密码不一致！')
            continue
        admin = Admin(name=name, pwd=generate_password_hash(pwd), is_super=True, role_id=role.id)
        db.session.add(admin)
        db.session.commit()
        print('管理员创建成功！！')
        return ''
