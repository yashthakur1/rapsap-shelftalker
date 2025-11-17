"""
Offer model definition using Pydantic.
Defines the structure of offer data with validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class OfferBase(BaseModel):
    """Base offer model with common fields"""
    product_id: str
    product_name: str
    brand: str
    offer_type: str  # e.g., "Discount", "Promo", "Seasonal"
    offer_details: str  # e.g., "20% off"
    price: float
    mrp: Optional[float] = None
    valid_till: str  # ISO format date
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
                "product_name": "Wireless Headphones",
                "brand": "TechBrand",
                "offer_type": "Discount",
                "offer_details": "20% off",
                "price": 4999,
                "mrp": 6999,
                "valid_till": "2025-12-31",
                "custom_fields": {}
            }
        }
