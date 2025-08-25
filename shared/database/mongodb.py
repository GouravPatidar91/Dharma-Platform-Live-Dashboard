"""MongoDB connection manager and utilities."""

import asyncio
from typing import Optional, Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import structlog

logger = structlog.get_logger(__name__)


class MongoDBManager:
    """MongoDB connection manager with connection pooling."""
    
    def __init__(self, connection_string: str, database_name: str):
        self.connection_string = connection_string
        self.database_name = database_name
        self.client: Optional[AsyncIOMotorClient] = None
        self.database: Optional[AsyncIOMotorDatabase] = None
        self._connected = False
    
    async def connect(self) -> None:
        """Establish connection to MongoDB."""
        try:
            self.client = AsyncIOMotorClient(
                self.connection_string,
                maxPoolSize=50,
                minPoolSize=10,
                maxIdleTimeMS=30000,
                waitQueueTimeoutMS=5000,
                serverSelectionTimeoutMS=5000,
            )
            
            # Test connection
            await self.client.admin.command('ping')
            self.database = self.client[self.database_name]
            self._connected = True
            
            logger.info("Connected to MongoDB", database=self.database_name)
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error("Failed to connect to MongoDB", error=str(e))
            raise
    
    async def disconnect(self) -> None:
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            self._connected = False
            logger.info("Disconnected from MongoDB")
    
    async def health_check(self) -> bool:
        """Check MongoDB connection health."""
        try:
            if not self._connected or not self.client:
                return False
            
            await self.client.admin.command('ping')
            return True
            
        except Exception as e:
            logger.error("MongoDB health check failed", error=str(e))
            return False
    
    async def create_indexes(self) -> None:
        """Create database indexes for optimal performance."""
        if not self.database:
            raise RuntimeError("Database not connected")
        
        # Posts collection indexes
        posts = self.database.posts
        await posts.create_index([("platform", 1), ("timestamp", -1)])
        await posts.create_index([("user_id", 1), ("timestamp", -1)])
        await posts.create_index([("analysis_results.sentiment", 1), ("timestamp", -1)])
        await posts.create_index([("analysis_results.risk_score", -1)])
        await posts.create_index([("content", "text")])
        await posts.create_index([("geolocation.coordinates", "2dsphere")])
        
        # Campaigns collection indexes
        campaigns = self.database.campaigns
        await campaigns.create_index([("status", 1), ("detection_date", -1)])
        await campaigns.create_index([("coordination_score", -1)])
        await campaigns.create_index([("participants", 1)])
        
        # User profiles collection indexes
        user_profiles = self.database.user_profiles
        await user_profiles.create_index([("platform", 1), ("user_id", 1)], unique=True)
        await user_profiles.create_index([("bot_probability", -1)])
        await user_profiles.create_index([("username", 1)])
        
        logger.info("MongoDB indexes created successfully")
    
    async def insert_post(self, post_data: Dict[str, Any]) -> str:
        """Insert a new post document."""
        if not self.database:
            raise RuntimeError("Database not connected")
        
        result = await self.database.posts.insert_one(post_data)
        return str(result.inserted_id)
    
    async def find_posts(
        self, 
        filter_query: Dict[str, Any], 
        limit: int = 100,
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        """Find posts matching the filter criteria."""
        if not self.database:
            raise RuntimeError("Database not connected")
        
        cursor = self.database.posts.find(filter_query).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
    
    async def update_post_analysis(
        self, 
        post_id: str, 
        analysis_results: Dict[str, Any]
    ) -> bool:
        """Update post with analysis results."""
        if not self.database:
            raise RuntimeError("Database not connected")
        
        result = await self.database.posts.update_one(
            {"_id": post_id},
            {"$set": {"analysis_results": analysis_results}}
        )
        return result.modified_count > 0
    
    async def insert_campaign(self, campaign_data: Dict[str, Any]) -> str:
        """Insert a new campaign document."""
        if not self.database:
            raise RuntimeError("Database not connected")
        
        result = await self.database.campaigns.insert_one(campaign_data)
        return str(result.inserted_id)
    
    async def get_active_campaigns(self) -> List[Dict[str, Any]]:
        """Get all active campaigns."""
        if not self.database:
            raise RuntimeError("Database not connected")
        
        cursor = self.database.campaigns.find({"status": "active"})
        return await cursor.to_list(length=None)