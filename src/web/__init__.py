from flask import Flask
from src.input_processing.processor import InputProcessor
from src.llm_pool.llm_pool import LLMPool
from src.moderator.moderator import Moderator
from src.heuristics.principles import Principles

def create_app(config):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a real secret key

    # Initialize components
    app.input_processor = InputProcessor()
    app.llm_pool = LLMPool(config['llm'])
    app.principles = Principles(config['principles']['version_control_file'])
    app.moderator = Moderator(app.llm_pool, app.principles)

    from src.web import routes
    app.register_blueprint(routes.bp)

    return app
