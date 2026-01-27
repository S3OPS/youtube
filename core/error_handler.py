"""
Error Handler
Centralized error handling utilities for consistent error management
"""

from functools import wraps
from .logging import get_logger
from .exceptions import YouTubeAutomationError


logger = get_logger(__name__)


def handle_errors(error_type=None, default_return=None, log_error=True, reraise=False):
    """Decorator for consistent error handling
    
    Args:
        error_type: Specific exception type to catch (catches all if None)
        default_return: Value to return on error
        log_error: Whether to log the error
        reraise: Whether to re-raise the exception after handling
        
    Returns:
        Decorated function with error handling
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if error_type and not isinstance(e, error_type):
                    raise
                
                if log_error:
                    logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                
                if reraise:
                    raise
                
                return default_return
        
        return wrapper
    return decorator


def safe_execute(func, *args, default=None, log_errors=True, **kwargs):
    """Execute a function with error handling
    
    Args:
        func: Function to execute
        *args: Positional arguments for the function
        default: Default value to return on error
        log_errors: Whether to log errors
        **kwargs: Keyword arguments for the function
        
    Returns:
        Function result or default value on error
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if log_errors:
            logger.error(f"Error executing {func.__name__}: {str(e)}", exc_info=True)
        return default


class ErrorContext:
    """Context manager for error handling with cleanup
    
    Usage:
        with ErrorContext("Operation name", cleanup_func=cleanup):
            # do work
            pass
    """
    
    def __init__(self, operation_name, cleanup_func=None, reraise=True):
        """Initialize error context
        
        Args:
            operation_name: Name of the operation for logging
            cleanup_func: Optional cleanup function to call on error
            reraise: Whether to re-raise exceptions
        """
        self.operation_name = operation_name
        self.cleanup_func = cleanup_func
        self.reraise = reraise
        self.logger = get_logger(__name__)
    
    def __enter__(self):
        self.logger.debug(f"Starting: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.logger.error(
                f"Error in {self.operation_name}: {exc_val}",
                exc_info=(exc_type, exc_val, exc_tb)
            )
            
            if self.cleanup_func:
                try:
                    self.cleanup_func()
                except Exception as cleanup_error:
                    self.logger.error(f"Cleanup failed: {cleanup_error}")
            
            return not self.reraise
        
        self.logger.debug(f"Completed: {self.operation_name}")
        return False
