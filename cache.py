import redis
import json
import logging
from config import Config

logger = logging.getLogger(__name__)


class RedisCache:
    """Redis cache manager for weather data"""
    
    def __init__(self):
        """Initialize Redis connection"""
        self.client = None
        self.enabled = True
        try:
            self.client = redis.Redis(
                host=Config.REDIS_HOST,
                port=Config.REDIS_PORT,
                password=Config.REDIS_PASSWORD if Config.REDIS_PASSWORD else None,
                db=Config.REDIS_DB,
                decode_responses=True,
                socket_connect_timeout=5
            )
            # Test connection
            self.client.ping()
            logger.info("Redis cache connected successfully")
        except (redis.ConnectionError, redis.TimeoutError) as e:
            logger.warning(f"Redis connection failed: {e}. Cache will be disabled.")
            self.enabled = False
            self.client = None
    
    def get(self, key):
        """
        Get value from cache
        
        Args:
            key (str): Cache key
            
        Returns:
            dict or None: Cached data or None if not found
        """
        if not self.enabled or not self.client:
            return None
        
        try:
            cached_data = self.client.get(key)
            if cached_data:
                logger.info(f"Cache HIT for key: {key}")
                return json.loads(cached_data)
            logger.info(f"Cache MISS for key: {key}")
            return None
        except Exception as e:
            logger.error(f"Error getting from cache: {e}")
            return None
    
    def set(self, key, value, expiration=None):
        """
        Set value in cache with expiration
        
        Args:
            key (str): Cache key
            value (dict): Data to cache
            expiration (int): Expiration time in seconds
        """
        if not self.enabled or not self.client:
            return False
        
        try:
            expiration = expiration or Config.CACHE_EXPIRATION
            serialized_value = json.dumps(value)
            self.client.setex(key, expiration, serialized_value)
            logger.info(f"Cached data for key: {key} with expiration: {expiration}s")
            return True
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False
    
    def delete(self, key):
        """
        Delete key from cache
        
        Args:
            key (str): Cache key to delete
        """
        if not self.enabled or not self.client:
            return False
        
        try:
            self.client.delete(key)
            logger.info(f"Deleted cache key: {key}")
            return True
        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")
            return False
    
    def clear_all(self):
        """Clear all keys from the current database"""
        if not self.enabled or not self.client:
            return False
        
        try:
            self.client.flushdb()
            logger.info("Cleared all cache")
            return True
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False
    
    def get_stats(self):
        """Get cache statistics"""
        if not self.enabled or not self.client:
            return {"enabled": False}
        
        try:
            info = self.client.info('stats')
            return {
                "enabled": True,
                "total_keys": self.client.dbsize(),
                "hits": info.get('keyspace_hits', 0),
                "misses": info.get('keyspace_misses', 0)
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"enabled": True, "error": str(e)}
