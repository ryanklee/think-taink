import logging
from flask import Flask
from src.web import create_app
from config.config_loader import load_config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
config = load_config()

# Create Flask app
app = create_app(config)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
