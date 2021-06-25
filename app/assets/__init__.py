from .route import assets_bp


def init_app(app):
    app.register_blueprint(assets_bp, url_prefix='/api')
