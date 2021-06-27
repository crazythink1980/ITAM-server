from .route import place_bp


def init_app(app):
    app.register_blueprint(place_bp, url_prefix='/api')