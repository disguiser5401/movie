from .movie_blue import blue_index, blue_movie
from .user_blue import blue_user


def init_home_blue(app):
    app.register_blueprint(blue_index)
    app.register_blueprint(blue_movie)
    app.register_blueprint(blue_user)
