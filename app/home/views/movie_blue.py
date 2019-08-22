from flask import render_template, Blueprint, session, request, redirect, url_for, flash, jsonify
from app.home.models.user_models import User
from app.home.models.movie_models import Movie, Tag, Banner
from app.home.models.operation_models import Comment, Collection, Score
from .user_blue import blue_user
from app.extensions import db, redis_store
from app.home.forms import CommentForm
from uuid import uuid4
from datetime import datetime

blue_index = Blueprint('blue_index', __name__)  # 首页
blue_movie = Blueprint('blue_movie', __name__, url_prefix='/movie')  # 电影


@blue_index.context_processor
@blue_movie.context_processor
@blue_user.context_processor
def tpl_extra():
    tags = Tag.query.all()
    user_id = session.get('user_id', '')
    data = {'user': User.query.get(user_id), 'tags': tags}
    return data


@blue_index.route('/')
def index():
    banners = Banner.query.all()
    hot_movies = Movie.query.all()[:8]
    return render_template('home/index.html', banners=banners, hot_movies=hot_movies)


@blue_movie.route('/list/<int:tag_id>/<int:page>/')
def movie_list(tag_id, page):
    sort = request.args.get('sort')
    if sort == 'comment_num':
        page_data = Movie.query.filter_by(tag_id=tag_id).order_by(Movie.comment_num.desc()).paginate(page=page, per_page=10)
    elif sort == 'play_num':
        page_data = Movie.query.filter_by(tag_id=tag_id).order_by(Movie.play_num.desc()).paginate(page=page, per_page=10)
    elif sort == 'release_time':
        page_data = Movie.query.filter_by(tag_id=tag_id).order_by(Movie.release_time.desc()).paginate(page=page, per_page=10)
    elif sort == 'star':
        page_data = Movie.query.filter_by(tag_id=tag_id).order_by(Movie.star.desc()).paginate(page=page, per_page=10)
    else:
        page_data = Movie.query.filter_by(tag_id=tag_id).paginate(page=page, per_page=10)
    return render_template('home/movie_list.html', page_data=page_data, tag_id=tag_id, sort=sort)


@blue_movie.route('/search/<int:page>')
def search(page):
    title = request.args.get('title', '')
    page_data = Movie.query.filter(Movie.title.like('%{}%'.format(title))).paginate(page=page, per_page=10)
    return render_template('home/search.html', page_data=page_data, title=title)


@blue_movie.route('/detail/<int:movie_id>/', methods=['GET', 'POST'])
def detail(movie_id):
    form = CommentForm()
    movie = Movie.query.get_or_404(movie_id)
    is_collect = Collection.query.filter_by(movie_id=movie.id, user_id=session.get('user_id', '')).count()
    if request.method == 'GET':
        movie.play_num += 1
        db.session.add(movie)
        db.session.commit()
        return render_template('home/detail.html', movie=movie, form=form, is_collect=is_collect)
    if 'user' in session and form.validate_on_submit():
        comment = Comment(
            user_id=session['user_id'],
            content=form.data['input_content'],
            movie_id=movie_id
        )
        movie.comment_num += 1
        db.session.add(movie)
        db.session.add(comment)
        db.session.commit()
        flash('评论成功！！！', 'comment_success')
        return redirect(url_for('blue_movie.detail', movie_id=movie.id))


@blue_movie.route('/collect/<int:movie_id>', methods=['POST'])
def collect(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        msg = '电影信息错误'
        info = 'err'
    elif 'user' not in session:
        msg = '登录后才能收藏'
        info = 'login_required'
    else:
        collection = Collection.query.filter_by(movie_id=movie.id, user_id=session['user_id']).first()
        if collection:
            db.session.delete(collection)
            movie.collect_num -= 1
            msg = '取消收藏成功'
            info = 'cancel'
        else:
            collection = Collection(movie_id=movie.id, user_id=session['user_id'])
            movie.collect_num += 1
            msg = '收藏成功'
            info = 'collect'
            db.session.add(collection)
        db.session.add(movie)
        db.session.commit()
    return jsonify({'info': info, 'msg': msg})


@blue_movie.route('/score/<int:movie_id>', methods=['POST'])
def score(movie_id):
    movie = Movie.query.get(movie_id)
    star = request.form.get('star')
    if (not movie) or (star not in ['1', '2', '3', '4', '5']):
        status = 'err'
        msg = '信息错误'
    elif 'user' not in session:
        msg = '登录后才能评分'
        status = 'err'
    else:
        _score = Score.query.filter_by(movie_id=movie.id, user_id=session['user_id']).first()
        if _score:
            msg = '你已经评分过该电影'
            status = 'err'
        else:
            _score = Score(movie_id=movie.id, user_id=session['user_id'], star=star)
            db.session.add(_score)
            db.session.commit()
            status = 'ok'
            msg = '评分成功'
            score_list = [int(i.star) for i in movie.scores]
            movie.star = round(sum(score_list) / len(score_list))
            db.session.add(movie)
            db.session.commit()
    return jsonify({'status': status, 'msg': msg})


@blue_movie.route('/danmu/v3/', methods=['GET', 'POST'])
def danmu():
    import json
    if 'user' not in session:
        return jsonify({'code': 1, 'data': []})
    if request.method == 'GET':
        movie_id = request.args.get('id')
        key = 'movie' + movie_id
        if redis_store.llen(key):
            data = [json.loads(i) for i in redis_store.lrange(key, 0, 300)]
        else:
            data = []
        return jsonify({'code': 0, 'data': data})
    else:
        data = json.loads(request.get_data())
        msg = {
            'author': data['author'],
            'color': data['color'],
            'time': data['time'],
            'player': data['id'],
            'text': data['text'],
            'type': data['type'],
            'ip': request.remote_addr,
            '_v': 0,
            '_id': datetime.now().strftime('%Y%m%d%H%M%S') + uuid4().hex,
        }
        redis_store.lpush('movie'+data['id'], json.dumps([data['time'], data['type'], data['color'], data['author'], data['text']]))
        return jsonify({'code': 0, 'data': msg})

