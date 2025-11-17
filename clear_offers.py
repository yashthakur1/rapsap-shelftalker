#!/usr/bin/env python
"""
Script to clear all offers from MongoDB database.
Run this before re-uploading CSV to avoid duplicates.
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient


async def clear_offers():
    """Clear all offers from the database"""
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    
    try:
        client = AsyncIOMotorClient(mongo_uri)
        db = client.aops_db
        
        # Count offers before deletion
        count_before = await db.offers.count_documents({})
        print(f"📊 Offers before deletion: {count_before}")
        
        if count_before == 0:
            print("✓ Database is already empty. Nothing to delete.")
            return
        
        # Delete all offers
        result = await db.offers.delete_many({})
        print(f"✓ Deleted {result.deleted_count} offers from database")
        
        # Verify deletion
        count_after = await db.offers.count_documents({})
        print(f"✓ Offers after deletion: {count_after}")
        
        client.close()
        print("✓ Database connection closed")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        raise


if __name__ == "__main__":
    print("=" * 50)
    print("AOPS - Clear All Offers from Database")
    print("=" * 50)
    print()
    
    asyncio.run(clear_offers())
