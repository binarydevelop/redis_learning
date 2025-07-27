import redis
import aioredis
from dotenv import load_dotenv
from os import getenv
from threading import Lock
from utils import retry_decorator 
load_dotenv()

class RedisSingleton:
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._redis_client = None
                    cls._instance._async_redis_client = None
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._connect()
            self._initialized = True
    
    @retry_decorator.retry()
    def _connect(self):
        """Establish Redis connection"""
        try:
            self._redis_client = redis.Redis(
                host=getenv("REDIS_HOST", "localhost"),
                port=int(getenv("REDIS_PORT", 6379)),
                username=getenv("REDIS_USERNAME"),
                password=getenv("REDIS_PASSWORD"),
                decode_responses=True,
            )
            # Test the connection
            self._redis_client.ping()
            print('Redis connected successfully')
            
        except Exception as e:
            self._redis_client = None
            raise ConnectionError(e)

    @retry_decorator.retry()
    async def _connect_async(self):
        """Establish async Redis connection"""
        try:
            self._async_redis_client = await aioredis.from_url(
                f"redis://{getenv('REDIS_HOST', 'localhost')}:{getenv('REDIS_PORT', 6379)}",
                username=getenv("REDIS_USERNAME"),
                password=getenv("REDIS_PASSWORD"),
                decode_responses=True,
            )
            # Test the connection
            await self._async_redis_client.ping()
            print('Async Redis connected successfully')
            
        except Exception as e:
            self._async_redis_client = None
            raise ConnectionError(e)
    
    def get_client(self):
        """Get the Redis client instance"""
        return self._redis_client
    
    async def get_async_client(self):
        """Get the async Redis client instance"""
        if self._async_redis_client is None:
            await self._connect_async()
        return self._async_redis_client
    
    def is_connected(self):
        """Check if Redis is connected"""
        if self._redis_client is None:
            return False
        try:
            self._redis_client.ping()
            return True
        except:
            return False

    async def is_async_connected(self):
        """Check if async Redis is connected"""
        if self._async_redis_client is None:
            return False
        try:
            await self._async_redis_client.ping()
            return True
        except:
            return False

# Global singleton instance
redis_singleton = RedisSingleton()

# Convenience function for easy access from any file
def get_redis():
    """Get Redis client - use this in any file that needs Redis"""
    return redis_singleton.get_client()

async def get_async_redis():
    """Get async Redis client - use this in any file that needs async Redis"""
    return await redis_singleton.get_async_client()

def is_redis_connected():
    """Check if Redis is connected - use this in any file"""
    return redis_singleton.is_connected()

async def is_async_redis_connected():
    """Check if async Redis is connected - use this in any file"""
    return await redis_singleton.is_async_connected()

