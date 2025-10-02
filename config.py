import os

class Config:
    """Production configuration"""

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)

    # Session configuration
    SESSION_COOKIE_SECURE = True  # HTTPS only
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes

    # Performance
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year cache for static files

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # Allow HTTP in development
