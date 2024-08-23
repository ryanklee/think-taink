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
    
    # Replace API keys with environment variables for all LLM providers
    for provider in config.keys():
        if 'api_key' in config[provider]:
            env_var_name = f'{provider.upper()}_API_KEY'
            config[provider]['api_key'] = os.getenv(env_var_name, config[provider]['api_key'])
    
    return config
