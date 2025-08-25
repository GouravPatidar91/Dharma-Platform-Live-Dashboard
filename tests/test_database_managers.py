"""Tests for database managers."""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from shared.database.redis import RedisManager


@pytest.mark.asyncio
async def test_redis_manager_connection():
    """Test Redis manager connection."""
    manager = RedisManager("redis://localhost:6379")
    
    # Mock the Redis client
    manager.client = AsyncMock()
    manager.client.ping = AsyncMock(return_value=True)
    manager._connected = True
    
    # Test health check
    health = await manager.health_check()
    assert health is True
    
    # Test set/get operations
    await manager.set("test_key", "test_value")
    manager.client.set.assert_called_once()
    
    manager.client.get = AsyncMock(return_value="test_value")
    value = await manager.get("test_key")
    assert value == "test_value"


@pytest.mark.asyncio
async def test_redis_manager_json_operations():
    """Test Redis manager JSON serialization."""
    manager = RedisManager("redis://localhost:6379")
    manager.client = AsyncMock()
    manager._connected = True
    
    # Test JSON serialization
    test_data = {"key": "value", "number": 42}
    await manager.set("json_key", test_data)
    
    # Verify JSON was serialized
    call_args = manager.client.set.call_args
    assert '"key": "value"' in call_args[0][1]
    assert '"number": 42' in call_args[0][1]


def test_redis_manager_initialization():
    """Test Redis manager initialization."""
    manager = RedisManager("redis://localhost:6379", max_connections=50)
    assert manager.redis_url == "redis://localhost:6379"
    assert manager.max_connections == 50
    assert manager._connected is False