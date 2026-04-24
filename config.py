"""
Configuration management for Malicious URL Detector
Supports environment variables and default values
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration"""
    
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = FLASK_ENV == 'development'
    
    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Models
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/rf_model_v2.pkl')
    ENCODER_PATH = os.getenv('ENCODER_PATH', 'models/label_encoder.pkl')
    MODEL_URL = os.getenv('MODEL_URL', '')
    ENCODER_URL = os.getenv('ENCODER_URL', '')
    AUTO_DOWNLOAD_MODELS = os.getenv('AUTO_DOWNLOAD_MODELS', 'false').lower() == 'true'
    MODEL_DOWNLOAD_TIMEOUT = int(os.getenv('MODEL_DOWNLOAD_TIMEOUT', 120))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Trusted domains
    TRUSTED_DOMAINS = {
        'google', 'youtube', 'facebook', 'twitter', 'instagram',
        'linkedin', 'microsoft', 'apple', 'amazon', 'netflix',
        'github', 'wikipedia', 'reddit', 'yahoo', 'bing', 'adobe',
        'dropbox', 'spotify', 'paypal', 'ebay', 'whatsapp',
        'telegram', 'zoom', 'slack', 'wordpress', 'shopify', 'salesforce'
    }
    
    # Suspicious keywords for URL analysis
    SUSPICIOUS_KEYWORDS = [
        'login', 'verify', 'secure', 'account', 'update', 'banking', 
        'confirm', 'password', 'signin', 'wallet', 'free', 'lucky', 
        'winner', 'click', 'setup', 'install'
    ]


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True


# Configuration selection
config_name = os.getenv('FLASK_ENV', 'production')
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

current_config = config_map.get(config_name, ProductionConfig)
