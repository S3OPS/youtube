"""
Custom Exceptions
Standardized exception hierarchy for the YouTube automation system
"""


class YouTubeAutomationError(Exception):
    """Base exception for all YouTube automation errors"""
    pass


class ConfigurationError(YouTubeAutomationError):
    """Raised when configuration is invalid or missing"""
    pass


class ContentGenerationError(YouTubeAutomationError):
    """Raised when content generation fails"""
    pass


class VideoCreationError(YouTubeAutomationError):
    """Raised when video creation fails"""
    pass


class UploadError(YouTubeAutomationError):
    """Raised when YouTube upload fails"""
    pass


class AuthenticationError(YouTubeAutomationError):
    """Raised when authentication fails"""
    pass


class CacheError(YouTubeAutomationError):
    """Raised when cache operations fail"""
    pass
