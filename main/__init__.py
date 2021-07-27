from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import ConfigNames

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config: ConfigNames = ConfigNames.DEVELOPMENT) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config.value)

    db.init_app(app)
    bcrypt.init_app(app)

    return app
