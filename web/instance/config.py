import os

POSTGRES_DEFAULT_USER = 'postgres'
POSTGRES_USER = 'flask'
POSTGRES_DB = 'flask-db'
POSTGRES_PASSWORD = 'flask'

class Config(object):
    """Parent configuration class."""
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    TOP_LEVEL_DIR = os.path.abspath(os.curdir)
    DEBUG = False
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BCRYPT_LOG_ROUNDS = 15
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + POSTGRES_USER + ':' + POSTGRES_PASSWORD + '@postgres:5432/' + POSTGRES_DB

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        'postgresql://' + POSTGRES_USER + ':' + POSTGRES_PASSWORD + '@postgres:5432/' + POSTGRES_DB + '-test'
    )
    DEBUG = True

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
