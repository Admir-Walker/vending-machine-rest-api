import os 

from flask import Flask
from flask_migrate import Migrate

from main import create_app, db
from config import ConfigNames

from main.models import User

app = create_app(ConfigNames.from_str(os.getenv('CONFIG_TYPE', 'DEVELOPMENT')))

migrate = Migrate(app, db)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
