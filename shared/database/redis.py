"""Redis connection manager and utilities."""

import json
from typing import Optional, Any, Dict, List, Union
import redis.asyncio as redis
from redis.asyncio import ConnectionPool
import structlog

logger = structlog.get_logger(__name__)


class RedisManager:
    """Redis connection manager with connection pooling."""
    
    def __init__(self, redis_url: str, max_connections: int = 20):
        self.redis_url = redis_url
        self.max_connections = max_connections
        self.pool: Optional[ConnectionPool] = None
        self.client: Optional[redis.Redis] = None
        self._connected = False
    
    async def connect(self) -> None:
        """Establish connection to Redis."""
        try:
            self.pool = ConnectionPool.from_url(
                self.redis_url,
                max_connections=self.max_connections,
                decode_responses=True,
                socket_keepalive=True,
                socket_keepalive_options={},
                health_check_interval=30,
            )
            
            self.client = redis.Redis(connection_pool=self.pool)
            
            # Test connection
            await self.client.ping()
            self._connected = True
            
            logger.info("Connected to Redis", url=self.redis_url)
            
        except Exception as e:
            logger.error("Failed to connect to Redis", error=str(e))
            raise
    
    async def disconnect(self) -> None:
        """Close Redis connection."""
        if self.client:
            await self.client.close()
            self._connected = False
            logger.info("Disconnected from Redis")
    
    async def health_check(self) -> bool:
        """Check Redis connection health."""
        try:
            if not self._connected or not self.client:
                return False
            
            await self.client.ping()
            return True
            
        except Exception as e:
            logger.error("Redis health check failed", error=str(e))
            return False
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        expire: Optional[int] = None
    ) -> bool:
        """Set a key-value pair with optional expiration."""
        if not self.client:
            raise RuntimeError("Redis not connected")
        
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            result = await self.client.set(key, value, ex=expire)
            return result is True
            
        except Exception as e:
            logger.error("Redis set failed", key=key, error=str(e))
            return False
    
    async def get(self, key: str, default: Any = None) -> Any:
        """Get value by key."""
        if not self.client:
            raise RuntimeError("Redis not connected")
        
        try:
            value = await self.client.get(key)
            if value is None:
                return default
            
            # Try to parse as JSON
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
                
        except Exception as e:
            logger.error("Redis get failed", key=key, error=str(e))
            return default
    
    async def delete(self, *keys: str) -> int:
        """Delete one or more keys."""
        if not self.client:
            raise RuntimeError("Redis not connected")
        
        try:
            return await self.client.delete(*keys)
        except Exception as e:
            logger.error("Redis delete failed", keys=keys, error=str(e))
            return 0
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        if not self.client:
            raise RuntimeError("Redis not connected")
        
        try:
            return await self.client.exists(key) > 0
        except Exception as e:
            logger.error("Redis exists failed", key=key, error=str(e))
            return False
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration for a key."""
        if not self.client:
            raise RuntimeError("Redis not connected")
        
        try:
            return await self.client.expire(key, seconds)
        except Exception as e:
            logger.error("Redis expire failed", key=key, error=str(e))
            return False
    
    async def incr(self, key: str, amount: int = 1) -> int:
        """Increment a key's value."""
        if not self.client:
            raise RuntimeError("Redis not connected")
        
        try:
            return await self.client.incr(key, amount)
        except Exception as e:
            logger.error("Redis incr failed", key=key, error=str(e))
            return 0
    
    async def lpush(self, key: str, *values: Any) -> int:
        """Push values to the left of a list."""
        if not self.client:
            raise RuntimeError("Redis not connected")
        
        try:
            serialized_values = []
            for value in values:
                if isinstance(value, (dict, list)):
                    serialized_values.append(json.dumps(value))
                else:
                    serialized_values.append(str(value))
            
            return await self.client.lpush(key, *serialized_values)
        except Exception as e:
            logger.error("Redis lpush failed", key=key, error=str(e))
            return 0
    
    async def rpop(self, key: str) -> Any:
        """Pop value from the right of a list."""
        if not self.client:
            raise RuntimeError("Redis not connected")
        
        try:
            value = await self.client.rpop(key)
            if value is None:
                return None
            
            # Try to parse as JSON
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
                
        except Exception as e:
            logger.error("Redis rpop failed", key=key, error=str(e))
            return None
    
    async def publish(self, channel: str, message: Any) -> int:
        """Publish message to a channel."""
        if not self.client:
            raise RuntimeError("Redis not connected")
        
        try:
            if isinstance(message, (dict, list)):
                message = json.dumps(message)
            
            return await self.client.publish(channel, message)
        except Exception as e:
            logger.error("Redis publish failed", channel=channel, error=str(e))
            return 0
    
    async def subscribe(self, *channels: str):
        """Subscribe to channels."""
        if not self.client:
            raise RuntimeError("Redis not connected")
        
        pubsub = self.client.pubsub()
        await pubsub.subscribe(*channels)
        return pubsub