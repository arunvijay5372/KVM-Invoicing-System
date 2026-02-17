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

    @login_manager.unauthorized_handler
    def unauthorized():
        from flask import request as req, jsonify, redirect, url_for
        if req.path.startswith('/api/'):
            return jsonify({'error': 'Authentication required'}), 401
        return redirect(url_for('auth.login', next=req.url))

    # ---------- Register blueprints ----------
    from app.routes.web import web_bp
    from app.routes.api import api_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # ---------- Create tables & seed admin user ----------
    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()
        _seed_defaults()

    return app


def _seed_defaults():
    """Create admin user and default data if they don't exist yet."""
    from app.models import User, Brand, Variant, Size, Product, Inventory

    # Admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@kvmenterprises.com')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

    # Default brands
    if not Brand.query.first():
        for name, code in [('Finolex', 'FIN'), ('Star', 'STR'),
                           ('Trubore', 'TRU'), ('K-Star', 'KST')]:
            db.session.add(Brand(name=name, code=code, description=f'{name} Pipes'))
        db.session.commit()

    # Default variants
    if not Variant.query.first():
        db.session.add_all([Variant(name='4kg', weight_kg=4.0),
                            Variant(name='6kg', weight_kg=6.0)])
        db.session.commit()

    # Default sizes
    if not Size.query.first():
        db.session.add_all([Size(size_inches=float(i)) for i in range(4, 13)])
        db.session.commit()

    # Auto-create products (Brand × Variant × Size) with inventory if none exist
    if not Product.query.first():
        brands = Brand.query.all()
        variants = Variant.query.all()
        sizes = Size.query.all()
        for brand in brands:
            for variant in variants:
                for size in sizes:
                    name = f"{brand.name} {variant.name} {int(size.size_inches)}\" Pipe"
                    product = Product(
                        name=name,
                        brand_id=brand.id,
                        variant_id=variant.id,
                        size_id=size.id,
                    )
                    db.session.add(product)
                    db.session.flush()
                    db.session.add(Inventory(product_id=product.id, quantity=0, reorder_level=10))
        db.session.commit()
