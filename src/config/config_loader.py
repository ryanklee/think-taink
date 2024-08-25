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
    
    # Load OpenAI API key from environment variable
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    # Log the API key (first few characters) for debugging
    print(f"API Key loaded (first 5 chars): {api_key[:5]}...")

    # Ensure the 'llm' key exists in the config
    if 'llm' not in config:
        config['llm'] = {}
    
    # Add the API key to the 'llm' configuration
    config['llm']['api_key'] = api_key
    
    return config
