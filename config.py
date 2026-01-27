"""
Configuration Management Module
Centralized configuration handling for the automation system
"""

import os
from dotenv import load_dotenv
from utils import validate_api_key


class Config:
    """Configuration manager for the automation system"""
    
    # Allowed configuration keys that can be updated via API
    UPDATABLE_KEYS = {'content_topic', 'content_frequency', 'video_privacy'}
    
    # AI Model configuration
    DEFAULT_MODEL = "gpt-3.5-turbo"
    DEFAULT_MAX_TOKENS_SCRIPT = 500
    DEFAULT_MAX_TOKENS_METADATA = 300
    DEFAULT_MAX_TOKENS_KEYWORDS = 150
    
    def __init__(self, config_dict=None):
        """Initialize configuration from environment or provided dict"""
        load_dotenv()
        
        if config_dict is None:
            config_dict = self._load_from_env()
        
        self.config = config_dict
        self._validate_config()
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        return {
            'openai_api_key': os.getenv('OPENAI_API_KEY'),
            'amazon_affiliate_tag': os.getenv('AMAZON_AFFILIATE_TAG', 'youraffid-20'),
            'content_topic': os.getenv('CONTENT_TOPIC', 'technology'),
            'content_frequency': os.getenv('CONTENT_FREQUENCY', 'daily'),
            'video_output_dir': os.getenv('VIDEO_OUTPUT_DIR', 'generated_videos'),
            'youtube_client_secrets': os.getenv('YOUTUBE_CLIENT_SECRETS', 'client_secrets.json'),
            'video_privacy': os.getenv('VIDEO_PRIVACY', 'public'),
            'ai_model': os.getenv('AI_MODEL', self.DEFAULT_MODEL)
        }
    
    def _validate_config(self):
        """Validate critical configuration values"""
        # Only validate API key if it's set (might not be for some operations)
        if self.config.get('openai_api_key'):
            try:
                validate_api_key(self.config['openai_api_key'], "OpenAI API key")
            except ValueError:
                # Don't fail on missing API key during initialization
                # It will fail later when actually needed
                pass
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def update(self, updates):
        """Update configuration with validation
        
        Args:
            updates: Dictionary of configuration updates
            
        Returns:
            Tuple of (success: bool, error_message: str or None)
        """
        # Validate that only allowed keys are being updated
        invalid_keys = set(updates.keys()) - self.UPDATABLE_KEYS
        if invalid_keys:
            return False, f"Cannot update keys: {', '.join(invalid_keys)}"
        
        # Update configuration
        for key, value in updates.items():
            if key in self.UPDATABLE_KEYS:
                self.config[key] = value
        
        return True, None
    
    def to_dict(self):
        """Return configuration as dictionary (without sensitive data)"""
        safe_config = self.config.copy()
        # Remove sensitive keys
        safe_config.pop('openai_api_key', None)
        return safe_config
