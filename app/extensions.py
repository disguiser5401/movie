from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_redis import FlaskRedis
import os
from datetime import datetime
from uuid import uuid4

db = SQLAlchemy()
migrate = Migrate()
sess = Session()
redis_store = FlaskRedis()


def init_extension(app):
    db.init_app(app)
    sess.init_app(app)
    redis_store.init_app(app)
    migrate.init_app(app, db)


def change_filename(filename):
    file_info = os.path.splitext(filename)[-1]
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + uuid4().hex + file_info
    return filename
