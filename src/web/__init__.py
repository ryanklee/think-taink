from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.input_processing.processor import InputProcessor
from src.llm_pool.llm_pool import LLMPool
from src.moderator.moderator import Moderator
from src.heuristics.principles import Principles
from .models import db

def create_app(config):
    app = Flask(__name__)
    app.config.from_mapping(config)
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get('database_uri', 'sqlite:///thinktank.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
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

    with app.app_context():
        db.create_all()

    from src.web import routes
    app.register_blueprint(routes.bp)

    return app
