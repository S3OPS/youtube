"""
Base Classes
Common base classes providing shared functionality
"""

from abc import ABC, abstractmethod
from .logging import get_logger
from .error_handler import handle_errors


class BaseService(ABC):
    """Abstract base class for all services"""
    
    def __init__(self, config=None):
        """Initialize service with configuration
        
        Args:
            config: Configuration dictionary or Config object
        """
        self.config = config or {}
        self.logger = get_logger(self.__class__.__name__)
    
    @abstractmethod
    def validate_config(self):
        """Validate service configuration
        
        Returns:
            Tuple of (is_valid: bool, error_message: str or None)
        """
        pass
    
    def get_config(self, key, default=None):
        """Get configuration value
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        if hasattr(self.config, 'get'):
            return self.config.get(key, default)
        return self.config.get(key, default) if isinstance(self.config, dict) else default


class BaseAPIClient(BaseService):
    """Base class for API clients with authentication"""
    
    def __init__(self, api_key=None, config=None):
        """Initialize API client
        
        Args:
            api_key: API key for authentication
            config: Configuration dictionary or Config object
        """
        super().__init__(config)
        self._api_key = api_key
        self._authenticated = False
    
    @property
    def api_key(self):
        """Get API key"""
        return self._api_key
    
    @api_key.setter
    def api_key(self, value):
        """Set API key and reset authentication"""
        self._api_key = value
        self._authenticated = False
    
    @abstractmethod
    def authenticate(self):
        """Authenticate with the API
        
        Returns:
            True if authentication successful, False otherwise
        """
        pass
    
    def is_authenticated(self):
        """Check if client is authenticated
        
        Returns:
            True if authenticated, False otherwise
        """
        return self._authenticated


class BaseProcessor(BaseService):
    """Base class for processors that transform data"""
    
    @abstractmethod
    def process(self, input_data):
        """Process input data
        
        Args:
            input_data: Input to process
            
        Returns:
            Processed output
        """
        pass
    
    @handle_errors(default_return=None, log_error=True)
    def safe_process(self, input_data):
        """Process with error handling
        
        Args:
            input_data: Input to process
            
        Returns:
            Processed output or None on error
        """
        return self.process(input_data)
