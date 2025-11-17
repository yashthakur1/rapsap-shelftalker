"""
PDF Generation API routes.
Handles PDF generation and rendering.
"""

from fastapi import APIRouter, HTTPException, Body
from typing import List
from datetime import datetime

from app.services.db import get_db
from app.services.pdfgen import get_pdf_service
from app.services.storage import get_storage_service

router = APIRouter(prefix="/pdf", tags=["pdf"])


@router.post("/generate")
async def generate_pdf(
    offer_ids: List[str] = Body(..., embed=False),
    template_id: str = Body(...),
    layout_options: dict = Body(default=None)
):
    """
    Generate PDF with selected offers using specified template.
    
    Request Body:
    {
        "offer_ids": ["id1", "id2", ...],
        "template_id": "template_mongodb_id",
        "layout_options": {
            "pageSize": "A4",
            "perPage": 24,
            "orientation": "portrait"
        }
    }
    
    Returns: { pdf_url: str, file_path: str, file_size: int }
    """
    try:
        # Validate input
        if not offer_ids:
            raise HTTPException(status_code=400, detail="No offers selected")
        
        if not template_id:
            raise HTTPException(status_code=400, detail="Template ID required")
        
        # Fetch offers from database
        db = await get_db()
        offers = await db.get_offers_by_ids(offer_ids)
        
        if not offers:
            raise HTTPException(status_code=404, detail="No offers found")
        
        # Fetch template (try ObjectId lookup, then fallback to string `id` field)
        template = await db.get_template_by_id(template_id)
        if not template:
            try:
                # Fallback lookup in case templates were stored with a string 'id' field
                tmpl = await db.db.templates.find_one({"id": template_id})
                if tmpl:
                    template = tmpl
            except Exception as _:
                template = None

        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        # Prepare layout options
        layout_options = layout_options or template.get("layout_options", {
            "pageSize": "A4",
            "perPage": 24,
            "orientation": "portrait"
        })
        
        # Get template HTML content
        template_html = template.get("html_content")
        if not template_html and template.get("file_path"):
            # Try to read from file path
            storage = get_storage_service()
            try:
                template_html = await storage.read_template_file(
                    f"{template['file_path']}/index.html"
                )
            except:
                template_html = None
        
        if not template_html:
            raise HTTPException(status_code=400, detail="Template has no HTML content")
        
        # Generate PDF
        pdf_service = get_pdf_service()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"offers_{timestamp}.pdf"
        
        pdf_path = await pdf_service.generate_batch_pdf(
            offers=offers,
            template_html=template_html,
            layout_options=layout_options,
            output_filename=output_filename
        )
        
        # Get file size
        import os
        file_size = os.path.getsize(pdf_path)
        
        # Return download info
        return {
            "status": "success",
            "pdf_url": pdf_service.get_pdf_download_url(output_filename),
            "file_path": pdf_path,
            "file_size": file_size,
            "offer_count": len(offers),
            "timestamp": timestamp
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"✗ Error generating PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")


@router.post("/preview")
async def preview_pdf(
    offer_ids: List[str] = Body(..., embed=False),
    template_id: str = Body(...),
    layout_options: dict = Body(default=None)
):
    """
    Generate a preview of the PDF without saving.
    
    Returns: { html_preview: str }
    """
    try:
        # Fetch offers
        db = await get_db()
        offers = await db.get_offers_by_ids(offer_ids[:1])  # Preview with first offer only
        
        if not offers:
            raise HTTPException(status_code=404, detail="Offers not found")
        
        # Fetch template
        template = await db.get_template_by_id(template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")

        # Determine layout options (use template defaults when not provided)
        layout_options = layout_options or template.get("layout_options") or {
            "pageSize": "A4",
            "perPage": 24,
            "orientation": "portrait"
        }
        if not isinstance(layout_options, dict):
            layout_options = {"pageSize": layout_options}

        pdf_service = get_pdf_service()
        page_size_info = pdf_service._resolve_page_size(layout_options.get("pageSize"))

        # Render preview with the same context as PDF generation so width/height are honored
        template_html = template.get("html_content", "")
        context = {
            "offers": offers,
            "layout": layout_options,
            "total_offers": len(offers),
            "page_size_css": page_size_info["css"],
            "label_width": page_size_info["label_width"],
            "label_height": page_size_info["label_height"]
        }
        html_preview = pdf_service.render_template(template_html, context)
        
        return {
            "status": "success",
            "html_preview": html_preview,
            "offer_count": len(offers)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"✗ Error generating preview: {e}")
        raise HTTPException(status_code=500, detail="Error generating preview")
