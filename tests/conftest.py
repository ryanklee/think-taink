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
    })
    yield app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.fixture(scope='session')
def live_server(app):
    return app
