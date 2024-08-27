import pytest
from src.main import create_app

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.fixture(scope='session')
def live_server(app):
    return app
