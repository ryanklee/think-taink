import sys
import os
import pytest

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import create_app
from src.config.config_loader import load_config

@pytest.fixture(scope='session')
def app():
    config = load_config()
    app = create_app(config)
    app.config.update({
        "TESTING": True,
        "SERVER_NAME": "localhost.localdomain",  # Add this line
    })
    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

from types import SimpleNamespace

@pytest.fixture(scope='session')
def live_server(app):
    with app.test_client() as client:
        server = SimpleNamespace(app=app, client=client)
        yield server
