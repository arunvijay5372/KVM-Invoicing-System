import os


def _fix_db_uri(uri):
    """Render gives postgres:// but SQLAlchemy 1.4+ needs postgresql://"""
    if uri and uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)
    return uri


class Config:
    """Base configuration"""
    SQLALCHEMY_DATABASE_URI = _fix_db_uri(
        os.getenv('DATABASE_URL', 'sqlite:///kvm_inventory.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
