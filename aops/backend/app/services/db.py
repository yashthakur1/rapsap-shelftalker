"""
Database service module.
Handles all MongoDB operations using Motor async client.
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from contextlib import asynccontextmanager
from typing import List, Optional, Dict, Any
from pymongo.errors import BulkWriteError


class DatabaseService:
    """Service for MongoDB operations using Motor async client"""

    def __init__(self, mongo_uri: Optional[str] = None):
        """
        Initialize database service.
        
        Args:
            mongo_uri: MongoDB connection string. Defaults to env var or local MongoDB.
        """
        self.mongo_uri = mongo_uri or os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[Any] = None

    async def connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(self.mongo_uri)
            self.db = self.client.aops_db
            
            # Create indexes for better query performance
            await self._create_indexes()
            print("✓ Connected to MongoDB")
        except Exception as e:
            print(f"✗ MongoDB connection failed: {e}")
            raise

    async def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("✓ Disconnected from MongoDB")

    async def _create_indexes(self):
        """Create database indexes for collections"""
        try:
            offers_collection = self.db.offers
            templates_collection = self.db.templates
            
            # Offers indexes
            await offers_collection.create_index([("product_id", ASCENDING)], unique=True)
            await offers_collection.create_index([("created_at", ASCENDING)])
            
            # Templates indexes
            await templates_collection.create_index([("name", ASCENDING)])
            await templates_collection.create_index([("is_preset", ASCENDING)])
            
            print("✓ Database indexes created")
        except Exception as e:
            print(f"⚠ Index creation warning: {e}")

    # ==================== OFFERS OPERATIONS ====================

    async def save_offers_bulk(self, offers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Insert multiple offers into the database.
        
        Args:
            offers: List of offer dictionaries
            
        Returns:
            Number of inserted documents
        """
        if not offers:
            return {"inserted_count": 0, "duplicates": []}

        try:
            # Use unordered inserts so one duplicate doesn't abort the whole batch.
            result = await self.db.offers.insert_many(offers, ordered=False)
            inserted = len(result.inserted_ids)
            return {"inserted_count": inserted, "duplicates": []}
        except BulkWriteError as bwe:
            # BulkWriteError.details contains useful counters and writeErrors
            details = getattr(bwe, "details", {}) or {}
            inserted = details.get("nInserted", 0)
            write_errors = details.get("writeErrors", []) or []

            # Collect duplicate product_ids when possible
            dup_ids = []
            for we in write_errors:
                # Prefer op.product_id, fallback to keyValue
                op = we.get("op") or {}
                key_value = we.get("keyValue") or {}
                pid = op.get("product_id") or key_value.get("product_id")
                if pid:
                    dup_ids.append(pid)

            print(f"⚠ BulkWriteError while inserting offers: inserted={inserted}, duplicates={dup_ids}")
            return {"inserted_count": inserted, "duplicates": dup_ids}
        except Exception as e:
            print(f"✗ Error inserting offers: {e}")
            raise

    async def get_offers(
        self, 
        skip: int = 0, 
        limit: int = 50,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve offers with pagination.
        
        Args:
            skip: Number of documents to skip
            limit: Maximum documents to return
            filter_dict: Optional MongoDB filter query
            
        Returns:
            List of offer documents
        """
        try:
            query = filter_dict or {}
            cursor = self.db.offers.find(query).skip(skip).limit(limit)
            return await cursor.to_list(length=limit)
        except Exception as e:
            print(f"✗ Error fetching offers: {e}")
            raise

    async def get_offer_by_id(self, offer_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single offer by ID.
        
        Args:
            offer_id: ObjectId as string
            
        Returns:
            Offer document or None if not found
        """
        try:
            from bson.objectid import ObjectId
            return await self.db.offers.find_one({"_id": ObjectId(offer_id)})
        except Exception as e:
            print(f"✗ Error fetching offer: {e}")
            return None

    async def get_offers_by_ids(self, offer_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Retrieve multiple offers by their IDs.
        
        Args:
            offer_ids: List of offer ObjectIds as strings
            
        Returns:
            List of offer documents
        """
        try:
            from bson.objectid import ObjectId
            object_ids = [ObjectId(oid) for oid in offer_ids]
            cursor = self.db.offers.find({"_id": {"$in": object_ids}})
            return await cursor.to_list(length=len(offer_ids))
        except Exception as e:
            print(f"✗ Error fetching offers by ids: {e}")
            raise

    async def count_offers(self, filter_dict: Optional[Dict[str, Any]] = None) -> int:
        """
        Count total offers matching filter.
        
        Args:
            filter_dict: Optional MongoDB filter query
            
        Returns:
            Total count
        """
        try:
            query = filter_dict or {}
            return await self.db.offers.count_documents(query)
        except Exception as e:
            print(f"✗ Error counting offers: {e}")
            return 0

    async def delete_all_offers(self) -> int:
        """
        Delete all offers from the database.
        
        Returns:
            Number of deleted documents
        """
        try:
            result = await self.db.offers.delete_many({})
            return result.deleted_count
        except Exception as e:
            print(f"✗ Error deleting offers: {e}")
            raise

    # ==================== TEMPLATES OPERATIONS ====================

    async def save_template(self, template: Dict[str, Any]) -> str:
        """
        Insert a new template.
        
        Args:
            template: Template document dictionary
            
        Returns:
            Inserted document ID
        """
        try:
            result = await self.db.templates.insert_one(template)
            return str(result.inserted_id)
        except Exception as e:
            print(f"✗ Error saving template: {e}")
            raise

    async def get_templates(self) -> List[Dict[str, Any]]:
        """
        Retrieve all templates (preset and custom).
        
        Returns:
            List of template documents
        """
        try:
            cursor = self.db.templates.find({}).sort("is_preset", -1)
            return await cursor.to_list(length=None)
        except Exception as e:
            print(f"✗ Error fetching templates: {e}")
            raise

    async def get_template_by_id(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single template by ID.
        
        Args:
            template_id: ObjectId as string
            
        Returns:
            Template document or None if not found
        """
        try:
            from bson.objectid import ObjectId
            return await self.db.templates.find_one({"_id": ObjectId(template_id)})
        except Exception as e:
            print(f"✗ Error fetching template: {e}")
            return None

    async def get_preset_templates(self) -> List[Dict[str, Any]]:
        """
        Retrieve only preset templates.
        
        Returns:
            List of preset template documents
        """
        try:
            cursor = self.db.templates.find({"is_preset": True})
            return await cursor.to_list(length=None)
        except Exception as e:
            print(f"✗ Error fetching preset templates: {e}")
            raise

    async def update_template_layout(self, template_id: str, layout_options: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update layout_options for a template document.

        Args:
            template_id: Template ObjectId as string
            layout_options: New layout options dict

        Returns:
            Updated template document or None
        """
        try:
            from bson.objectid import ObjectId
            from datetime import datetime

            # Defensive sanitization of incoming id (strip whitespace and surrounding quotes)
            tid = str(template_id).strip()
            if (tid.startswith('"') and tid.endswith('"')) or (tid.startswith("'") and tid.endswith("'")):
                tid = tid[1:-1]

            try:
                oid = ObjectId(tid)
            except Exception:
                # If conversion fails, try with original tid
                oid = None

            if oid is not None:
                # Defensive unwrap: if caller passed nested { layout_options: {...} }, extract inner dict
                lo = layout_options
                if isinstance(lo, dict) and 'layout_options' in lo and isinstance(lo.get('layout_options'), dict):
                    lo = lo.get('layout_options')

                result = await self.db.templates.update_one({"_id": oid}, {"$set": {"layout_options": lo, "updated_at": datetime.utcnow()}})
                if result.matched_count:
                    return await self.get_template_by_id(tid)

            # Fallback: try to update by matching string id field if present in documents
            # Fallback update by string id field; also defensively unwrap if nested
            lo2 = layout_options
            if isinstance(lo2, dict) and 'layout_options' in lo2 and isinstance(lo2.get('layout_options'), dict):
                lo2 = lo2.get('layout_options')

            result2 = await self.db.templates.update_one({"id": tid}, {"$set": {"layout_options": lo2, "updated_at": datetime.utcnow()}})
            if result2.matched_count:
                # Attempt to fetch by original tid or by querying the document that has id==tid
                doc = await self.db.templates.find_one({"id": tid})
                return doc

            return None
        except Exception as e:
            print(f"✗ Error updating template layout: {e}")
            raise


# Global database instance
db_service: Optional[DatabaseService] = None


async def init_db(mongo_uri: Optional[str] = None) -> DatabaseService:
    """Initialize global database service instance"""
    global db_service
    db_service = DatabaseService(mongo_uri)
    await db_service.connect()
    return db_service


async def get_db() -> DatabaseService:
    """Get the global database service instance"""
    if db_service is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return db_service


@asynccontextmanager
async def get_db_context():
    """Context manager for database operations"""
    db = await get_db()
    try:
        yield db
    except Exception as e:
        print(f"✗ Database context error: {e}")
        raise
