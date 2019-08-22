from redis import Redis
import datetime
import os


def get_db_uri(database):
    return '{}+{}://{}:{}@{}:{}/{}'.format(database['ENGINE'], database['DRIVER'], database['USER'], database['PASSWORD'], database['HOST'], database['PORT'], database['NAME'])


class Config(object):
    SECRET_KEY = 'yang'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'redis'


class DevelopConfig(Config):
    DEBUG = True
    DATABASE = {
        'ENGINE': 'mysql',
        'DRIVER': 'mysqldb',
        'USER': 'root',
        'PASSWORD': 'czp541632...',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'movie'
    }
    REDIS_URL = 'redis://localhost:6379/1'
    SESSION_REDIS = Redis(db=1)
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(hours=1)
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)
    MEDIA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/media/')


class TestingConfig(Config):
    TESTING = True
    DATABASE = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'movie'
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


class ProductConfig(Config):
    DATABASE = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'movie'
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


envs = {
    'develop': DevelopConfig,
    'testing': TestingConfig,
    'product': ProductConfig,
}

