from app.extensions import db
from datetime import datetime


# 会员
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text, default='')
    face = db.Column(db.String(255), default='default.jpg')
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    user_logs = db.relationship('UserLog', backref='user')
    comments = db.relationship('Comment', backref='user')
    collections = db.relationship('Collection', backref='user')
    scores = db.relationship('Score', backref='user')

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 会员登录日志
class UserLog(db.Model):
    __tablename__ = 'user_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(100))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    __mapper_args__ = {"order_by": add_time.desc()}

    def __repr__(self):
        return '<UserLog {}>'.format(self.id)
