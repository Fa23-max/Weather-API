import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class"""
    
    # Weather API Configuration
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    WEATHER_API_ENDPOINT = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
    
    # Redis Configuration
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    
    # Cache Configuration (in seconds)
    # Default: 12 hours = 43200 seconds
    CACHE_EXPIRATION = int(os.getenv('CACHE_EXPIRATION', 43200))
    
    # Flask Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    
    # Rate Limiting
    RATE_LIMIT = os.getenv('RATE_LIMIT', '100 per hour')
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        if not Config.WEATHER_API_KEY:
            raise ValueError("WEATHER_API_KEY is required. Please set it in your .env file")
        return True
