"""
Offer model definition using Pydantic.
Defines the structure of offer data with validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class OfferBase(BaseModel):
    """Base offer model with common fields"""
    categories: str  # Categories column from CSV
    brand: str  # Brand column from CSV
    item_name: str  # Item Name column from CSV
    mrp: float  # MRP column from CSV
    rapsap_price: float  # Rapsap Price column from CSV
    savings: float  # Savings column from CSV
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
                "categories": "Groceries",
                "brand": "TechBrand",
                "item_name": "Wireless Headphones",
                "mrp": 6999,
                "rapsap_price": 4999,
                "savings": 2000,
                "custom_fields": {}
            }
        }
