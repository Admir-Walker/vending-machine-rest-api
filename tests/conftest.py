import pytest
from main import create_app
from config import ConfigNames


@pytest.fixture
def app():
    app = create_app(ConfigNames.TESTING)

    with app.test_client() as client:
        with app.app_context():
            pass
        yield client