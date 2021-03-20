from flask import Flask


def init_app(app: Flask):
    from .user_view import bp_user

    app.register_blueprint(bp_user)