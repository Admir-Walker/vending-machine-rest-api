from main.controllers.user_controller import UserListResource
from main.controllers.auth_controller import LoginAuth
from flask_restful import Api
import pytest
from main import create_app, db
from config import ConfigNames


@pytest.fixture
def client():
    app = create_app(ConfigNames.TESTING)

    with app.test_client() as client:
            with app.app_context():
                db.create_all()
            yield client