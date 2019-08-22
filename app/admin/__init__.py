from .admin_blue import blue_admin


def init_admin_blue(app):
    app.register_blueprint(blue_admin)
