"""
Offer model definition using Pydantic.
Defines the structure of offer data with validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class OfferBase(BaseModel):
    """Base offer model with common fields"""
    product_id: str  # Product ID from CSV
    product_name: str  # Product Name from CSV
    brand: str  # Brand column from CSV
    offer_type: Optional[str] = None  # Offer Type from CSV
    offer_details: Optional[str] = None  # Offer Details from CSV
    price: float  # Sale price from CSV
    mrp: float  # MRP column from CSV
    valid_till: Optional[str] = None  # Expiry date from CSV
    custom_fields: Optional[Dict[str, Any]] = Field(default_factory=dict)


class OfferCreate(OfferBase):
    """Model for creating a new offer"""
    pass


class Offer(OfferBase):
    """Complete offer model with ID and timestamps"""
    id: Optional[str] = Field(None, alias="_id")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "product_id": "PRD-001",
                "product_name": "Natures Bake WW MG Burger Bun",
                "brand": "Nils Natures bake",
                "offer_type": "Discount",
                "offer_details": "Save ₹9",
                "price": 51,
                "mrp": 60,
                "valid_till": "2025-12-31",
                "custom_fields": {}
            }
        }
