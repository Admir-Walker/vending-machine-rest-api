from flask_apispec.extension import FlaskApiSpec
from flask_restful import Api
from main.utils.jwt import JWT
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import ConfigNames

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWT()

from main.utils.register_endpoints import register_api_endpoints, register_docs

def create_app(config: ConfigNames = ConfigNames.DEVELOPMENT) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config.value)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)


    api = Api(app)
    docs = FlaskApiSpec(app)

    register_api_endpoints(api)
    register_docs(docs)

    return app