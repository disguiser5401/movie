from flask import Flask
from settings import envs
from .extensions import init_extension
from .home.views import init_home_blue
from .admin import init_admin_blue
from .home.models import user_models, operation_models, movie_models
from .admin import models


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(envs['develop'])
    init_extension(app)
    init_home_blue(app)
    init_admin_blue(app)
    return app
