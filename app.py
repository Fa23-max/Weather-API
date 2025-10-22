from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from config import Config
from cache import RedisCache
from weather_service import WeatherService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Validate configuration
try:
    Config.validate()
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise

# Initialize services
cache = RedisCache()
weather_service = WeatherService()

# Initialize rate limiter with fallback to memory if Redis unavailable
try:
    if cache.enabled:
        # Try to use Redis for rate limiting
        limiter = Limiter(
            app=app,
            key_func=get_remote_address,
            default_limits=[Config.RATE_LIMIT],
            storage_uri=f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/{Config.REDIS_DB}"
        )
        logger.info("Rate limiter using Redis storage")
    else:
        raise Exception("Redis not available")
except Exception as e:
    # Fall back to in-memory rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[Config.RATE_LIMIT],
        storage_uri="memory://"
    )
    logger.warning(f"Rate limiter using in-memory storage (Redis unavailable)")


@app.route('/')
def home():
    """API home endpoint with usage information"""
    return jsonify({
        'message': 'Weather API',
        'version': '1.0.0',
        'endpoints': {
            '/': 'API information (this page)',
            '/health': 'Health check endpoint',
            '/weather/<location>': 'Get weather data for a location',
            '/cache/stats': 'Get cache statistics',
            '/cache/clear': 'Clear all cache (DELETE method)'
        },
        'usage': {
            'example': '/weather/London,UK',
            'parameters': {
                'unit': 'Optional - metric (default), us, or uk'
            }
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    cache_stats = cache.get_stats()
    rate_limiter_storage = "redis" if cache.enabled else "memory"
    return jsonify({
        'status': 'healthy',
        'cache': cache_stats,
        'rate_limiter': rate_limiter_storage
    })


@app.route('/weather/<path:location>')
@limiter.limit(Config.RATE_LIMIT)
def get_weather(location):
    """
    Get weather data for a location
    
    Args:
        location (str): Location name (e.g., "London,UK" or "New York")
        
    Query Parameters:
        unit (str): Unit system - 'metric' (default), 'us', or 'uk'
        format (str): Response format - 'full' or 'simple' (default)
    """
    if not location or location.strip() == '':
        return jsonify({
            'error': 'Location parameter is required',
            'example': '/weather/London,UK'
        }), 400
    
    # Get query parameters
    unit_group = request.args.get('unit', 'metric')
    response_format = request.args.get('format', 'simple')
    
    # Validate unit group
    if unit_group not in ['metric', 'us', 'uk']:
        return jsonify({
            'error': 'Invalid unit parameter',
            'valid_values': ['metric', 'us', 'uk']
        }), 400
    
    # Create cache key
    cache_key = f"weather:{location.lower()}:{unit_group}"
    
    # Try to get from cache
    cached_data = cache.get(cache_key)
    if cached_data:
        logger.info(f"Returning cached data for: {location}")
        return jsonify({
            'location': location,
            'cached': True,
            'data': cached_data
        })
    
    # Fetch from weather API
    logger.info(f"Fetching fresh data for: {location}")
    result = weather_service.get_weather(location, unit_group)
    
    # Handle errors
    if 'error' in result:
        status_code = result.get('status_code', 500)
        return jsonify({
            'error': result['error'],
            'location': location
        }), status_code
    
    # Format response
    weather_data = result['data']
    if response_format == 'simple':
        formatted_data = weather_service.format_weather_response(weather_data)
    else:
        formatted_data = weather_data
    
    # Cache the result
    cache.set(cache_key, formatted_data)
    
    return jsonify({
        'location': location,
        'cached': False,
        'data': formatted_data
    })


@app.route('/cache/stats')
def cache_stats():
    """Get cache statistics"""
    stats = cache.get_stats()
    return jsonify(stats)


@app.route('/cache/clear', methods=['DELETE'])
def clear_cache():
    """Clear all cache"""
    success = cache.clear_all()
    if success:
        return jsonify({
            'message': 'Cache cleared successfully'
        })
    else:
        return jsonify({
            'error': 'Failed to clear cache'
        }), 500


@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded"""
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': str(e.description)
    }), 429


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'Please check the API documentation at /'
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {e}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500


if __name__ == '__main__':
    logger.info(f"Starting Weather API on port {Config.PORT}")
    logger.info(f"Debug mode: {Config.DEBUG}")
    logger.info(f"Cache enabled: {cache.enabled}")
    
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.DEBUG
    )
