#!/usr/bin/env python
"""
Script to clear all templates from MongoDB database.
Run this to force re-initialization of preset templates.
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient


async def clear_templates():
    """Clear all templates from the database"""
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    
    try:
        client = AsyncIOMotorClient(mongo_uri)
        db = client.aops_db
        
        # Count templates before deletion
        count_before = await db.templates.count_documents({})
        print(f"📊 Templates before deletion: {count_before}")
        
        if count_before == 0:
            print("✓ Database is already empty. Nothing to delete.")
            return
        
        # Delete all templates
        result = await db.templates.delete_many({})
        print(f"✓ Deleted {result.deleted_count} templates from database")
        
        # Verify deletion
        count_after = await db.templates.count_documents({})
        print(f"✓ Templates after deletion: {count_after}")
        
        client.close()
        print("✓ Database connection closed")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        raise


if __name__ == "__main__":
    print("=" * 50)
    print("AOPS - Clear All Templates from Database")
    print("=" * 50)
    print()
    
    asyncio.run(clear_templates())
