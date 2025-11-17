"""
Templates API routes.
Handles template upload and retrieval.
"""

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime
from bson.objectid import ObjectId

from app.models.template import Template, TemplateCreate
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

router = APIRouter(prefix="/templates", tags=["templates"])


@router.post("/upload")
async def upload_template(file: UploadFile = File(...), name: str = "Custom Template"):
    """
    Upload a custom template as ZIP file (containing HTML and CSS).
    
    Parameters:
    - file: ZIP file containing template assets
    - name: Name for the template
    
    Returns: { template_id: str, name: str, file_path: str }
    """
    try:
        # Validate file type
        if not file.filename.endswith(".zip"):
            raise HTTPException(status_code=400, detail="File must be a ZIP archive")
        
        # Save and extract ZIP
        content = await file.read()
        storage = get_storage_service()
        extract_dir, html_file = await storage.save_template_zip(content, name)
        
        # Read HTML content if available
        html_content = None
        if html_file:
            html_content = await storage.read_template_file(html_file)
        
        # Save template metadata to database
        db = await get_db()
        template_doc = {
            "name": name,
            "description": f"Custom template uploaded at {datetime.utcnow().isoformat()}",
            "is_preset": False,
            "file_path": extract_dir,
            "html_content": html_content,
            "css_content": None,
            "layout_options": {
                "pageSize": "A4",
                "perPage": 24,
                "orientation": "portrait"
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        template_id = await db.save_template(template_doc)
        
        response_data = {
            "status": "success",
            "template_id": str(template_id),
            "name": name,
            "file_path": extract_dir
        }
        
        return JSONResponse(content=serialize_for_json(response_data))
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"✗ Error uploading template: {e}")
        raise HTTPException(status_code=500, detail=f"Error uploading template: {str(e)}")


@router.get("/")
async def get_templates():
    """
    Retrieve all available templates (preset and custom).
    
    Returns: { templates: list[Template] }
    """
    try:
        db = await get_db()
        templates = await db.get_templates()
        
        # Convert ObjectId to string and remove _id field
        for template in templates:
            if "_id" in template:
                template["id"] = str(template["_id"])
                del template["_id"]
        
        response_data = {
            "status": "success",
            "templates": templates,
            "total": len(templates)
        }
        
        return JSONResponse(content=serialize_for_json(response_data))
        
    except Exception as e:
        print(f"✗ Error fetching templates: {e}")
        raise HTTPException(status_code=500, detail="Error fetching templates")


@router.get("/preset")
async def get_preset_templates():
    """
    Retrieve only preset templates.
    
    Returns: { templates: list[Template] }
    """
    try:
        db = await get_db()
        templates = await db.get_preset_templates()
        
        # Convert ObjectId to string and remove _id field
        for template in templates:
            if "_id" in template:
                template["id"] = str(template["_id"])
                del template["_id"]
        
        response_data = {
            "status": "success",
            "templates": templates,
            "total": len(templates)
        }
        
        return JSONResponse(content=serialize_for_json(response_data))
        
    except Exception as e:
        print(f"✗ Error fetching preset templates: {e}")
        raise HTTPException(status_code=500, detail="Error fetching templates")


@router.get("/{template_id}")
async def get_template(template_id: str):
    """
    Retrieve a single template by ID.
    
    Path Parameters:
    - template_id: MongoDB ObjectId as string
    
    Returns: Template with full content
    """
    try:
        db = await get_db()
        template = await db.get_template_by_id(template_id)
        
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        if "_id" in template:
            template["id"] = str(template["_id"])
            del template["_id"]
        
        response_data = {
            "status": "success",
            "template": template
        }
        
        return JSONResponse(content=serialize_for_json(response_data))
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"✗ Error fetching template: {e}")
        raise HTTPException(status_code=500, detail="Error fetching template")


@router.put("/{template_id}/layout")
async def update_template_layout(template_id: str, layout_options: dict):
    """
    Update layout_options for a template.

    Body: { layout_options: { pageSize: {...}, perPage: n, orientation: 'portrait' } }
    """
    try:
        # Normalize incoming payload: allow either raw layout dict or wrapper { layout_options: {...} }
        payload = layout_options or {}
        # Unwrap if the client accidentally wrapped the layout under a `layout_options` key
        # Keep unwrapping until we reach a structure that looks like layout options (has pageSize or perPage)
        try:
            while isinstance(payload, dict) and 'layout_options' in payload and not ('pageSize' in payload or 'perPage' in payload):
                payload = payload.get('layout_options') or {}
        except Exception:
            payload = layout_options or {}

        db = await get_db()
        # Log incoming update attempt for easier debugging
        print(f"→ PUT /templates/{template_id}/layout payload: {payload}")

        updated = await db.update_template_layout(template_id, payload)
        if not updated:
            # Return helpful message when update did not match any document
            raise HTTPException(status_code=404, detail=f"Template not found or not updated (id={template_id})")

        if "_id" in updated:
            updated["id"] = str(updated["_id"])
            del updated["_id"]

        response_data = {"status": "success", "template": updated}
        return JSONResponse(content=serialize_for_json(response_data))
    except HTTPException:
        raise
    except Exception as e:
        print(f"✗ Error updating template layout: {e}")
        raise HTTPException(status_code=500, detail="Error updating template layout")
