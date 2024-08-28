import sys
import os
import pytest
import threading
from werkzeug.serving import make_server

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import create_app
from src.config.config_loader import load_config

# Mock API keys for testing
os.environ['OPENAI_API_KEY'] = 'test_openai_api_key'
os.environ['ANTHROPIC_API_KEY'] = 'test_anthropic_api_key'

class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()
        self.app = app

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()

@pytest.fixture(scope='session')
def app():
    config = load_config()
    app = create_app(config)
    app.config.update({
        "TESTING": True,
        "SERVER_NAME": "localhost:5000",
    })
    return app

@pytest.fixture(scope='session')
def live_server(app):
    server = ServerThread(app)
    server.start()
    yield server
    server.shutdown()

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()
