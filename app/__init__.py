import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name=None):
    """Flask application factory"""
    app = Flask(__name__)

    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    from config import config as cfg_map
    app.config.from_object(cfg_map.get(config_name, cfg_map['default']))

    # ---------- Database ----------
    db.init_app(app)

    # ---------- Login manager ----------
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(user_id)

    # ---------- Register blueprints ----------
    from app.routes.web import web_bp
    from app.routes.api import api_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # ---------- Create tables on first request ----------
    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()

    return app
