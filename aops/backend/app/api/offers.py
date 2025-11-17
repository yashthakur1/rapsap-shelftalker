"""
Offers API routes.
Handles CSV uploads and offer retrieval.
"""

import csv
import io
import json
from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime
from bson.objectid import ObjectId

from app.models.offer import Offer, OfferCreate
from app.services.db import get_db
from app.services.storage import get_storage_service


def serialize_for_json(obj):
    """Custom JSON serializer for non-JSON types"""
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: serialize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_for_json(item) for item in obj]
    return obj

router = APIRouter(prefix="/offers", tags=["offers"])


@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload and parse CSV file containing offers.
    
    Expected CSV columns:
    product_id, product_name, brand, offer_type, offer_details, price, mrp, valid_till
    
    Returns: { inserted_count: int, preview: list[Offer] }
    """
    try:
        # Read and parse CSV
        content = await file.read()
        csv_text = content.decode("utf-8")
        csv_reader = csv.DictReader(io.StringIO(csv_text))
        
        if not csv_reader.fieldnames:
            raise HTTPException(status_code=400, detail="Invalid CSV format")
        
        # Parse offers
        offers = []
        for row in csv_reader:
            try:
                offer = {
                    "product_id": row.get("product_id", "").strip(),
                    "product_name": row.get("product_name", "").strip(),
                    "brand": row.get("brand", "").strip(),
                    "offer_type": row.get("offer_type", "").strip(),
                    "offer_details": row.get("offer_details", "").strip(),
                    "price": float(row.get("price", 0)),
                    "mrp": float(row.get("mrp", 0)) if row.get("mrp") else None,
                    "valid_till": row.get("valid_till", "").strip(),
                    "custom_fields": {},
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                
                # Validate with Pydantic model
                OfferCreate(**offer)
                offers.append(offer)
            except Exception as e:
                print(f"⚠ Skipping invalid row: {e}")
                continue
        
        if not offers:
            raise HTTPException(status_code=400, detail="No valid offers in CSV")

        # Save to database
        db = await get_db()
        inserted_result = await db.save_offers_bulk(offers)
        # inserted_result is a dict: { inserted_count: int, duplicates: list }
        inserted_count = int(inserted_result.get("inserted_count", 0))
        duplicates = inserted_result.get("duplicates", [])

        # Save file to storage
        storage = get_storage_service()
        await storage.save_csv_file(content, file.filename or "offers.csv")

        # Return preview (first 5 offers) - convert all non-JSON types
        preview = [serialize_for_json(offer) for offer in offers[:5]]

        response_data = {
            "status": "success",
            "inserted_count": inserted_count,
            "total_rows": len(offers),
            "preview": preview,
            "duplicates": duplicates
        }

        return JSONResponse(content=serialize_for_json(response_data))
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"✗ CSV upload error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")


@router.get("/")
async def get_offers(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    """
    Retrieve paginated list of offers.
    
    Query Parameters:
    - skip: Number of offers to skip (default: 0)
    - limit: Number of offers to return (default: 50, max: 100)
    
    Returns: { offers: list[Offer], total: int }
    """
    try:
        db = await get_db()
        offers = await db.get_offers(skip=skip, limit=limit)
        total = await db.count_offers()
        
        # Convert ObjectId to string and remove _id field
        for offer in offers:
            if "_id" in offer:
                offer["id"] = str(offer["_id"])
                del offer["_id"]
        
        response_data = {
            "status": "success",
            "offers": offers,
            "total": total,
            "skip": skip,
            "limit": limit
        }
        
        return JSONResponse(content=serialize_for_json(response_data))
        
    except Exception as e:
        print(f"✗ Error fetching offers: {e}")
        raise HTTPException(status_code=500, detail="Error fetching offers")


@router.get("/{offer_id}")
async def get_offer(offer_id: str):
    """
    Retrieve a single offer by ID.
    
    Path Parameters:
    - offer_id: MongoDB ObjectId as string
    
    Returns: Offer
    """
    try:
        db = await get_db()
        offer = await db.get_offer_by_id(offer_id)
        
        if not offer:
            raise HTTPException(status_code=404, detail="Offer not found")
        
        if "_id" in offer:
            offer["id"] = str(offer["_id"])
            del offer["_id"]
        
        response_data = {
            "status": "success",
            "offer": offer
        }
        
        return JSONResponse(content=serialize_for_json(response_data))
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"✗ Error fetching offer: {e}")
        raise HTTPException(status_code=500, detail="Error fetching offer")


@router.post("/clear-all")
async def clear_all_offers():
    """
    Delete all offers from the database.
    WARNING: This action cannot be undone.
    
    Returns: { deleted_count: int }
    """
    try:
        db = await get_db()
        
        # Count before deletion
        count_before = await db.count_offers()
        
        if count_before == 0:
            return JSONResponse(content={
                "status": "success",
                "message": "Database is already empty",
                "deleted_count": 0
            })
        
        # Delete all offers
        result = await db.delete_all_offers()
        
        print(f"✓ Cleared {result} offers from database")
        
        return JSONResponse(content={
            "status": "success",
            "message": f"Successfully deleted all offers",
            "deleted_count": result
        })
        
    except Exception as e:
        print(f"✗ Error clearing offers: {e}")
        raise HTTPException(status_code=500, detail=f"Error clearing offers: {str(e)}")
