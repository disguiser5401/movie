from app.extensions import db
from datetime import datetime


# 标签
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    movies = db.relationship('Movie', backref='tag')

    def __repr__(self):
        return '<Tag {}>'.format(self.name)


# 电影
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255))
    info = db.Column(db.Text)
    logo = db.Column(db.String(255))
    star = db.Column(db.SmallInteger)
    play_num = db.Column(db.BigInteger, default=0)
    comment_num = db.Column(db.BigInteger, default=0)
    collect_num = db.Column(db.BigInteger, default=0)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'))
    area = db.Column(db.String(255))
    release_time = db.Column(db.Date)
    length = db.Column(db.String(100))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    comments = db.relationship('Comment', backref='movie')
    collections = db.relationship('Collection', backref='movie')
    scores = db.relationship('Score', backref='movie')
    banner = db.relationship('Banner', backref='movie', uselist=False)

    __mapper_args__ = {"order_by": star.desc()}

    def __repr__(self):
        return '<Movie {}>'.format(self.title)


# 上映预告
class Banner(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id', ondelete='CASCADE'))
    logo = db.Column(db.String(255))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Banner {}>'.format(self.id)
