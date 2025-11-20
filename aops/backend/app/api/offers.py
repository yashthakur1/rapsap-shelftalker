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

        # Helper: normalize header names to a canonical key
        def normalize_key(k: str):
            return (k or '').strip().lower().replace('-', ' ').replace('_', ' ')

        # Mapping of possible header names to our internal field names
        header_map = {
            'product id': 'product_id',
            'id': 'product_id',
            'sku': 'product_id',
            'product_id': 'product_id',

            'product name': 'product_name',
            'productname': 'product_name',
            'item name': 'product_name',
            'itemname': 'product_name',
            'name': 'product_name',

            'brand': 'brand',

            'offer type': 'offer_type',
            'offertype': 'offer_type',
            'offer': 'offer_type',

            'offer details': 'offer_details',
            'offer_details': 'offer_details',
            'details': 'offer_details',
            'savings': 'offer_details',

            'price': 'price',
            'rapsap price': 'price',
            'sale price': 'price',

            'mrp': 'mrp',

            'valid till': 'valid_till',
            'valid_till': 'valid_till',
            'expiry': 'valid_till',
            'expiry date': 'valid_till'
        }

        # Build normalized header lookup for each CSV column
        normalized_headers = {}
        for h in csv_reader.fieldnames:
            nk = normalize_key(h)
            normalized_headers[h] = header_map.get(nk)

        # Simple slug generator for missing product_id
        def slugify(text: str):
            if not text:
                return ''
            s = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in text)
            s = '-'.join(s.lower().split())
            return s[:60]

        # Parse offers
        offers = []
        auto_idx = 1
        for row in csv_reader:
            try:
                mapped = {}
                custom = {}
                # Map known headers
                for raw_h, value in row.items():
                    val = (value or '').strip()
                    target = normalized_headers.get(raw_h)
                    if target:
                        mapped[target] = val
                    else:
                        # Keep leftover columns in custom_fields using their raw header
                        if val != '':
                            custom[raw_h.strip()] = val

                # Ensure required fields exist; generate product_id if missing
                product_name = mapped.get('product_name') or custom.get('Item Name') or ''
                product_id = mapped.get('product_id') or custom.get('product_id') or slugify(product_name) or f'auto-{auto_idx}'
                if product_id.startswith('auto-'):
                    auto_idx += 1

                # Parse numeric fields safely
                def to_float(x):
                    try:
                        return float(str(x).replace(',', '').strip()) if str(x).strip() != '' else 0.0
                    except:
                        return 0.0

                price = to_float(mapped.get('price') or custom.get('Rapsap Price') or mapped.get('rapsap price'))
                mrp = to_float(mapped.get('mrp') or custom.get('MRP') or mapped.get('MRP'))

                offer = {
                    'product_id': product_id,
                    'product_name': mapped.get('product_name') or product_name or product_id,
                    'brand': mapped.get('brand') or custom.get('Brand') or '',
                    'offer_type': mapped.get('offer_type') or '',
                    'offer_details': mapped.get('offer_details') or custom.get('Savings') or '',
                    'price': price,
                    'mrp': mrp,
                    'valid_till': mapped.get('valid_till') or '',
                    'custom_fields': custom,
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
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
