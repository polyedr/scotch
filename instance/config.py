# /instance/config.py


import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """Configurations for development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for testing with a separate test database"""
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgrespassword1@localhost:5432/test_db'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1@localhost:5432/test_db'

    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging"""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production"""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
