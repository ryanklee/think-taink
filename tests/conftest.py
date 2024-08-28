import sys
import os
import pytest

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import create_app
from src.config.config_loader import load_config

# Mock API keys for testing
os.environ['OPENAI_API_KEY'] = 'test_openai_api_key'
os.environ['ANTHROPIC_API_KEY'] = 'test_anthropic_api_key'

@pytest.fixture(scope='session')
def app():
    config = load_config()
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()
