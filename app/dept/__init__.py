from .route import dept_bp


def init_app(app):
    app.register_blueprint(dept_bp, url_prefix='/api')