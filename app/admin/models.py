from app.extensions import db
from datetime import datetime


# 权限
class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Auth {}>'.format(self.name)


# 角色
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    auth_list = db.Column(db.String(255))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    admins = db.relationship('Admin', backref='role')

    def __repr__(self):
        return '<Role {}>'.format(self.name)


# 管理员
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    admin_logs = db.relationship('AdminLog', backref='admin')
    operation_logs = db.relationship('OperationLog', backref='admin')

    def __repr__(self):
        return '<Admin {}>'.format(self.name)

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登陆日志
class AdminLog(db.Model):
    __tablename__ = 'admin_log'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id', ondelete='CASCADE'), )
    ip = db.Column(db.String(100))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    __mapper_args__ = {"order_by": add_time.desc()}

    def __repr__(self):
        return '<AdminLog {}>'.format(self.id)


# 操作日志
class OperationLog(db.Model):
    __tablename__ = 'operation_log'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id', ondelete='CASCADE'))
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)

    __mapper_args__ = {"order_by": add_time.desc()}

    def __repr__(self):
        return '<OperationLog {}>'.format(self.id)
