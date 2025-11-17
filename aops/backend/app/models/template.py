"""
Template model definition using Pydantic.
Defines the structure for preset and custom templates.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class TemplateBase(BaseModel):
    """Base template model"""
    name: str
    description: Optional[str] = None
    is_preset: bool = False  # True for preset templates, False for custom
    layout_options: Optional[Dict[str, Any]] = Field(
        default_factory=lambda: {
            "pageSize": "A4",
            "perPage": 24,
            "orientation": "portrait"
        }
    )


class TemplateCreate(TemplateBase):
    """Model for creating a new template"""
    html_content: Optional[str] = None
    css_content: Optional[str] = None


class Template(TemplateBase):
    """Complete template model with ID and metadata"""
    id: Optional[str] = Field(None, alias="_id")
    html_content: Optional[str] = None
    css_content: Optional[str] = None
    file_path: Optional[str] = None  # Path to uploaded ZIP or template files
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "Minimal Template",
                "description": "Simple clean offer tag",
                "is_preset": True,
                "layout_options": {
                    "pageSize": "A4",
                    "perPage": 24,
                    "orientation": "portrait"
                }
            }
        }
