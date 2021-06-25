from .route import users_bp


def init_app(app):
    app.register_blueprint(users_bp, url_prefix='/api')
