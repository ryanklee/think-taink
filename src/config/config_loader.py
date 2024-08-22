import yaml
import os

def load_config():
    """
    Load the configuration from the YAML file.
    
    Returns:
        dict: The configuration dictionary.
    """
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config
