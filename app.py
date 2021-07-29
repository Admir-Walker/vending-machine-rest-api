from http import HTTPStatus
import os

from flask_migrate import Migrate
from werkzeug.utils import redirect
from main import create_app, db
from main.models import User, Product
from config import ConfigNames


app = create_app(ConfigNames.from_str(os.getenv('CONFIG_TYPE', 'DEVELOPMENT')))

migrate = Migrate(app, db)


@app.route("/")
def index():
    return redirect('/swagger-ui'), HTTPStatus.PERMANENT_REDIRECT


if __name__ == '__main__':
    app.run()
