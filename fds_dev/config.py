import os
import yaml
from typing import Dict, Any

DEFAULT_CONFIG = {
    'language': {
        'source': 'auto',
        'target': 'en'
    },
    'rules': {},
    'translator': {
        'provider': 'echo'
    }
}

def find_config_file(path: str = '.') -> str:
    """
    Finds the .fdsrc.yaml file in the given path or its parent directories.
    """
    current_dir = os.path.abspath(path)
    while True:
        config_path = os.path.join(current_dir, '.fdsrc.yaml')
        if os.path.exists(config_path):
            return config_path
        
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir: # Reached the root directory
            return None
        current_dir = parent_dir

def load_config() -> Dict[str, Any]:
    """
    Loads the configuration from .fdsrc.yaml.
    Starts searching from the current working directory upwards.
    Returns default config if not found.
    """
    config_path = find_config_file()
    if config_path:
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)
                # Simple merge with default config
                config = DEFAULT_CONFIG.copy()
                config.update(user_config)
                return config
        except Exception as e:
            print(f"Error loading config file '{config_path}': {e}")
            return DEFAULT_CONFIG
    
    return DEFAULT_CONFIG

if __name__ == '__main__':
    # To test, you would need a .fdsrc.yaml file in this directory or a parent.
    # We can create a dummy one for the test.
    dummy_yaml = """
language:
  source: 'ko'
rules:
  require-section-license: on
"""
    with open('.fdsrc.yaml', 'w', encoding='utf-8') as f:
        f.write(dummy_yaml)

    config = load_config()
    print("Loaded configuration:")
    print(yaml.dump(config, default_flow_style=False))
    
    os.remove('.fdsrc.yaml') # Clean up the dummy file
