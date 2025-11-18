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
from app.config.branding import get_available_brands, get_brand_config, BRAND_CONFIGS


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
        
        # Use absolute path for uploads directory (important for Render persistent disk)
        # On Render with persistent disk at /opt/render/project/aops/backend/uploads
        # We need to resolve the correct path
        if os.getenv("UPLOADS_PATH"):
            uploads_base = os.getenv("UPLOADS_PATH")
        else:
            # Fallback: construct path relative to the app directory
            app_dir = os.path.dirname(os.path.abspath(__file__))  # .../aops/backend/app
            backend_dir = os.path.dirname(app_dir)  # .../aops/backend
            uploads_base = os.path.join(backend_dir, "uploads")
        
        print(f"→ Uploads base directory: {uploads_base}")
        
        init_pdf_service(output_dir=os.path.join(uploads_base, "pdfs"))
        init_storage_service(base_dir=uploads_base)
        
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
        from app.templates.preset_shelf_talker_minimal import PRESET_SHELF_TALKER_MINIMAL
        from app.templates.preset_shelf_talker_branded import PRESET_SHELF_TALKER_BRANDED
        from app.templates.preset_shelf_talker_loyal import PRESET_SHELF_TALKER_LOYAL
        
        # Delete all existing preset templates to ensure fresh initialization
        existing = await db.get_preset_templates()
        if len(existing) > 0:
            print(f"🔄 Clearing {len(existing)} existing preset templates for fresh initialization...")
            for template in existing:
                template_id = str(template.get("_id"))
                await db.db.templates.delete_one({"_id": template["_id"]})
            print("✓ Cleared old presets")
        
        templates_to_create = [
            PRESET_SHELF_TALKER_MINIMAL,
            PRESET_SHELF_TALKER_BRANDED,
            PRESET_SHELF_TALKER_LOYAL
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
            "health": "/health",
            "branding": "/branding"
        },
        "docs": "/docs"
    }


@app.get("/branding")
async def get_branding():
    """Get available branding configurations"""
    # Return full brand configurations directly so frontend receives complete objects
    try:
        brands = list(BRAND_CONFIGS.values())
        return {"status": "success", "brands": brands}
    except Exception:
        # Fallback to legacy method
        brands = get_available_brands()
        return {"status": "success", "brands": [get_brand_config(b) for b in brands]}


@app.get("/_debug/logos")
async def debug_logos():
    """Debug endpoint: list logo files visible to the server"""
    try:
        import os
        base = os.path.abspath(os.path.join(os.getcwd(), "app", "logos"))
        files = []
        if os.path.isdir(base):
            for fn in sorted(os.listdir(base)):
                fp = os.path.join(base, fn)
                files.append({"name": fn, "size": os.path.getsize(fp), "path": fp})
        return {"status": "ok", "dir": base, "files": files}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/_debug/uploads")
async def debug_uploads():
    """Debug endpoint: list uploads (PDFs, CSV, templates)"""
    try:
        if os.getenv("UPLOADS_PATH"):
            uploads_base = os.getenv("UPLOADS_PATH")
        else:
            app_dir = os.path.dirname(os.path.abspath(__file__))  # .../aops/backend/app
            backend_dir = os.path.dirname(app_dir)  # .../aops/backend
            uploads_base = os.path.join(backend_dir, "uploads")
        
        result = {
            "status": "ok",
            "uploads_path": uploads_base,
            "exists": os.path.isdir(uploads_base),
            "subdirs": {}
        }
        if os.path.isdir(uploads_base):
            for subdir in ["pdfs", "csv", "templates"]:
                subpath = os.path.join(uploads_base, subdir)
                if os.path.isdir(subpath):
                    files = []
                    try:
                        for fn in sorted(os.listdir(subpath))[-5:]:  # Last 5 files
                            fp = os.path.join(subpath, fn)
                            if os.path.isfile(fp):
                                files.append({"name": fn, "size": os.path.getsize(fp)})
                    except Exception as e:
                        files.append({"error": str(e)})
                    result["subdirs"][subdir] = files
        return result
    except Exception as e:
        return {"status": "error", "error": str(e)}


# Static file serving for PDFs and logos
# Use consistent absolute paths
try:
    if os.getenv("UPLOADS_PATH"):
        uploads_base = os.getenv("UPLOADS_PATH")
    else:
        # Construct path relative to app directory (this file's location)
        app_dir = os.path.dirname(os.path.abspath(__file__))  # .../aops/backend/app
        backend_dir = os.path.dirname(app_dir)  # .../aops/backend
        uploads_base = os.path.join(backend_dir, "uploads")
    
    if os.path.isdir(uploads_base):
        app.mount("/downloads", StaticFiles(directory=uploads_base), name="downloads")
        print(f"✓ Mounted /downloads → {uploads_base}")
    else:
        print(f"⚠ Uploads directory not found: {uploads_base}")
except Exception as e:
    print(f"⚠ Static file mounting warning: {e}")

try:
    # Use absolute path to the logos directory relative to this module
    logos_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "logos"))
    app.mount("/logos", StaticFiles(directory=logos_dir), name="logos")
except Exception as e:
    print(f"⚠ Logo static file mounting warning: {e}")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEBUG", "True").lower() == "true"
    )
