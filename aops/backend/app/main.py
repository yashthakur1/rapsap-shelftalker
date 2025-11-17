"""
FastAPI main application entry point.
Initializes routes, middleware, and startup/shutdown events.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime

from app.api import offers, templates, pdf
from app.services.db import init_db, get_db
from app.services.pdfgen import init_pdf_service
from app.services.storage import init_storage_service
from app.models.template import Template as TemplateModel


# Lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown.
    Initializes database and services on startup.
    """
    # Startup
    print("\n" + "="*50)
    print("🚀 Starting AOPS Backend Server...")
    print("="*50)
    
    try:
        # Initialize services
        mongo_uri = os.getenv("MONGODB_URI","mongodb+srv://pscode:prath%40123@movie.xvphk1n.mongodb.net/?retryWrites=true&w=majority&appName=movie")
        db = await init_db(mongo_uri)
        
        init_pdf_service(output_dir="./uploads/pdfs")
        init_storage_service(base_dir="./uploads")
        
        # Initialize preset templates
        await initialize_preset_templates(db)
        
        print("✓ All services initialized successfully")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"✗ Startup error: {e}")
        raise
    
    yield
    
    # Shutdown
    print("\n" + "="*50)
    print("🛑 Shutting down AOPS Backend Server...")
    print("="*50)
    try:
        db = await get_db()
        await db.disconnect()
        print("✓ Services cleaned up")
        print("="*50 + "\n")
    except Exception as e:
        print(f"⚠ Shutdown warning: {e}")


async def initialize_preset_templates(db):
    """Initialize preset templates in database if they don't exist"""
    try:
        from app.templates.preset_minimal import PRESET_MINIMAL_HTML
        from app.templates.preset_promo import PRESET_PROMO_HTML
        from app.templates.preset_multi import PRESET_MULTI_HTML
        from app.templates.preset_shelf_talker_minimal import PRESET_SHELF_TALKER_MINIMAL
        from app.templates.preset_shelf_talker_branded import PRESET_SHELF_TALKER_BRANDED
        
        # Delete all existing preset templates to ensure fresh initialization
        existing = await db.get_preset_templates()
        if len(existing) > 0:
            print(f"🔄 Clearing {len(existing)} existing preset templates for fresh initialization...")
            for template in existing:
                template_id = str(template.get("_id"))
                await db.db.templates.delete_one({"_id": template["_id"]})
            print("✓ Cleared old presets")
        
        templates_to_create = [
            {
                "name": "Minimal Clean",
                "description": "Simple, modern design with 4 columns per page",
                "is_preset": True,
                "html_content": PRESET_MINIMAL_HTML,
                "css_content": None,
                "layout_options": {
                    "pageSize": "A4",
                    "perPage": 24,
                    "orientation": "portrait"
                },
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Promotional Bold",
                "description": "Eye-catching promotional design with vibrant colors",
                "is_preset": True,
                "html_content": PRESET_PROMO_HTML,
                "css_content": None,
                "layout_options": {
                    "pageSize": "A4",
                    "perPage": 24,
                    "orientation": "portrait"
                },
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "name": "Detailed Multi-Column",
                "description": "Detailed design with pricing breakdown in 2 columns",
                "is_preset": True,
                "html_content": PRESET_MULTI_HTML,
                "css_content": None,
                "layout_options": {
                    "pageSize": "A4",
                    "perPage": 24,
                    "orientation": "portrait"
                },
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            PRESET_SHELF_TALKER_MINIMAL,
            PRESET_SHELF_TALKER_BRANDED
        ]
        
        for template in templates_to_create:
            # Add created_at/updated_at if not present (for dict templates)
            if "created_at" not in template:
                template["created_at"] = datetime.utcnow()
                template["updated_at"] = datetime.utcnow()
            
            template_id = await db.save_template(template)
            print(f"✓ Created preset template: {template['name']} ({template_id})")
        
    except Exception as e:
        print(f"⚠ Template initialization warning: {e}")


# Create FastAPI application
app = FastAPI(
    title="AOPS - Automated Offer Print System",
    description="Backend API for generating and printing offer tags from CSV",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS - Allow all origins in development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Include API routers
app.include_router(offers.router)
app.include_router(templates.router)
app.include_router(pdf.router)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AOPS Backend",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to AOPS Backend API",
        "version": "1.0.0",
        "endpoints": {
            "offers": "/docs#/offers",
            "templates": "/docs#/templates",
            "pdf": "/docs#/pdf",
            "health": "/health"
        },
        "docs": "/docs"
    }


# Static file serving for PDFs
try:
    app.mount("/downloads", StaticFiles(directory="./uploads"), name="downloads")
except Exception as e:
    print(f"⚠ Static file mounting warning: {e}")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEBUG", "True").lower() == "true"
    )
