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
    
    # Load API keys from environment variables
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY')

    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    if not anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
    
    # Log the API keys (first few characters) for debugging
    print(f"OpenAI API Key loaded (first 5 chars): {openai_api_key[:5]}...")
    print(f"Anthropic API Key loaded (first 5 chars): {anthropic_api_key[:5]}...")

    # Ensure the 'openai' and 'anthropic' keys exist in the config
    if 'openai' not in config:
        config['openai'] = {}
    if 'anthropic' not in config:
        config['anthropic'] = {}
    
    # Add the API keys to the respective configurations
    config['openai']['api_key'] = openai_api_key
    config['anthropic']['api_key'] = anthropic_api_key
    
    return config
