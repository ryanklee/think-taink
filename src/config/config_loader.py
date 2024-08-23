import yaml
import os
from dotenv import load_dotenv

def load_config():
    """
    Load the configuration from the YAML file and environment variables.
    
    Returns:
        dict: The configuration dictionary.
    """
    load_dotenv()  # Load environment variables from .env file

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    config_path = os.path.join(project_root, 'config', 'config.yaml')
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    # Replace ${OPENAI_API_KEY} with the actual environment variable
    config['openai']['api_key'] = os.getenv('OPENAI_API_KEY')
    
    return config
