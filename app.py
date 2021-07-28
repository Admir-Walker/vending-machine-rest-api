import os

from flask_migrate import Migrate
from main import create_app, db
from main.models import User, Product
from config import ConfigNames


app = create_app(ConfigNames.from_str(os.getenv('CONFIG_TYPE', 'DEVELOPMENT')))

migrate = Migrate(app, db)


@app.route("/")
def index():
    return 'Hi'


if __name__ == '__main__':
    app.run()
