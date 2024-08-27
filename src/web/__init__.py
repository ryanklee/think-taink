from flask import Flask
from src.input_processing.processor import InputProcessor
from src.llm_pool.llm_pool import LLMPool
from src.moderator.moderator import Moderator
from src.heuristics.principles import Principles

from src.llm_pool.llm_pool import LLMPool

def create_app(config):
    app = Flask(__name__)
    app.config.from_mapping(config)
    
    # Initialize LLM pools
    app.llm_pools = {
        'openai': LLMPool(config, api_type='openai'),
        'anthropic': LLMPool(config, api_type='anthropic')
    }
    app.config['SECRET_KEY'] = config.get('secret_key', 'your-secret-key')  # Replace with a real secret key

    # Initialize components
    app.input_processor = InputProcessor()
    app.llm_pool = LLMPool(config)
    app.principles = Principles(config['principles']['version_control_file'])
    app.moderator = Moderator(app.llm_pool, app.principles)

    from src.web import routes
    app.register_blueprint(routes.bp)

    return app
