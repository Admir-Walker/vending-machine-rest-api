from enum import Enum


class Config():
    TESTING = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = "secret"

    # Secret key for signing cookies
    SECRET_KEY = "secret"

    JWT_SECRET_KEY = 'super-secret'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''


class ConfigNames(Enum):
    PRODUCTION = ProductionConfig
    DEVELOPMENT = DevelopmentConfig
    TESTING = TestingConfig

    @staticmethod
    def from_str(label: str):
        label = label.upper()
        return ConfigNames[label]
