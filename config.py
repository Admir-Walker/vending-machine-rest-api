import os
from enum import Enum
from distutils.util import strtobool
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from dotenv import load_dotenv

load_dotenv()

# db settings
DB_ECHO = strtobool(os.environ.get('DB_ECHO', 'False'))
DB_TRACK_MODIFICATIONS = strtobool(
    os.environ.get('DB_TRACK_MODIFICATIONS', 'False'))
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'root')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = int(os.environ.get('DB_PORT', 5432))
DB_NAME = os.environ.get('DB_NAME', 'vending_machine')
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_TEST_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}_test"

# app keys settings

APP_CSRF_SESSION_KEY = os.environ.get('APP_CSRF_SESSION_KEY', 'secret')
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY', 'secret')
APP_JWT_SECRET_KEY = os.environ.get('APP_JWT_SECRET_KEY', 'secret')

spec = APISpec(
    title='Vending Machine Rest Api',
    version='1.0.0',
    openapi_version='2.0.2',
    plugins=[MarshmallowPlugin()]
)

api_key_scheme = {"type": "apiKey", "in": "header", "name": "Authorization"}

spec.components.security_scheme("Authorization", api_key_scheme)


class Config():
    TESTING = True
    DEBUG = True

    SQLALCHEMY_ECHO = DB_ECHO
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = DB_TRACK_MODIFICATIONS

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = APP_CSRF_SESSION_KEY

    # Secret key for signing cookies
    SECRET_KEY = APP_SECRET_KEY

    JWT_SECRET_KEY = APP_JWT_SECRET_KEY

    # Api config
    APISPEC_SPEC = spec
    APISPEC_SWAGGER_URL = '/swagger/'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = DB_URL


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = DB_TEST_URL


class ConfigNames(Enum):
    PRODUCTION = ProductionConfig
    DEVELOPMENT = DevelopmentConfig
    TESTING = TestingConfig

    @staticmethod
    def from_str(label: str):
        label = label.upper()
        return ConfigNames[label]
