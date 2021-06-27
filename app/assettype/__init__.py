from .route import asset_type_bp


def init_app(app):
    app.register_blueprint(asset_type_bp, url_prefix='/api')