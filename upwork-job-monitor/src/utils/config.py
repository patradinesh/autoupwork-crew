import os
import json
from dotenv import load_dotenv

def load_config(file_path=None):
    # Load environment variables from .env file
    load_dotenv()
    
    config = {}
    
    # Load file-based config if provided
    if file_path:
        try:
            with open(file_path, 'r') as f:
                config.update(json.load(f))
        except Exception as e:
            print(f"Error loading config file: {e}")
    
    # Override with environment variables
    config['upwork_username'] = os.environ.get('UPWORK_USERNAME')
    config['upwork_password'] = os.environ.get('UPWORK_PASSWORD')
    config['notification_email'] = os.environ.get('NOTIFICATION_EMAIL')
    config['notification_phone'] = os.environ.get('NOTIFICATION_PHONE')
    config['check_interval'] = int(os.environ.get('CHECK_INTERVAL', 60))
    config['api_key'] = os.environ.get('API_KEY')
    config['api_secret'] = os.environ.get('API_SECRET')
    
    return config

def get_upwork_credentials(config):
    return config.get('upwork', {}).get('credentials', {})

def get_notification_preferences(config):
    return config.get('notifications', {})

def save_config(file_path, config):
    with open(file_path, 'w') as f:
        json.dump(config, f, indent=4)