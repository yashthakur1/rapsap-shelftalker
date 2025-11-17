# AOPS Backend - AI Coding Agent Instructions

## Project Overview
AOPS (Automated Offer Print System) is a full-stack web application for batch-generating PDF offer tags from CSV files. It consists of:
- **Backend**: FastAPI (async Python) with Motor MongoDB driver
- **Frontend**: React 18 with Vite, Tailwind CSS, and Axios
- **Database**: MongoDB for offers and templates persistence

## Architecture Essentials

### Service-Based Backend Design
The backend uses a **layered service architecture** (see `aops/backend/app/`):
- **API Layer** (`api/*.py`): FastAPI routers handling HTTP requests
- **Service Layer** (`services/*.py`): Business logic and external integrations
  - `db.py`: Singleton MongoDB service with async Motor client
  - `pdfgen.py`: Jinja2 template rendering + Pyppeteer browser automation
  - `storage.py`: File I/O for uploads (CSV, PDFs, custom templates)
- **Models Layer** (`models/*.py`): Pydantic validation schemas

### Data Flow for Core Workflow
1. **CSV Upload** → `POST /offers/upload-csv` parses CSV, validates with Pydantic models, bulk-inserts to MongoDB, saves file
2. **Fetch Offers** → `GET /offers?skip=0&limit=50` queries MongoDB with pagination
3. **Generate PDF** → `POST /pdf/generate` fetches offers + template from DB, renders Jinja2 with context, uses Pyppeteer to convert HTML→PDF

## Critical Developer Workflows

### Starting Development
```powershell
# Backend (requires Python 3.8+, MongoDB running locally on :27017)
cd aops\backend
pip install -r requirements.txt
python run_backend.py  # Starts on http://127.0.0.1:8001

# Frontend (requires Node 16+)
cd aops\frontend
npm install
npm run dev  # Starts on http://localhost:5173
```

### Key Commands
- Backend health check: `curl http://localhost:8000/health`
- API docs: `http://localhost:8000/docs` (auto-generated Swagger)
- Frontend build for production: `npm run build` (output: `dist/`)

### Debugging Patterns
- **MongoDB errors**: Check `MONGODB_URI` env var (defaults to `mongodb://localhost:27017`)
- **PDF generation failures**: Often Pyppeteer issue—ensure Node.js compatibility and disk space
- **CORS errors**: Backend allows all origins in dev; check `app.main` for production config
- **Preset templates missing**: They're auto-created on startup from `app/templates/preset_*.py` files

## Project-Specific Conventions

### Database Service Pattern
The database service uses a **global singleton** pattern (not dependency injection):
```python
# Initialization in app.main.py startup
db = await init_db(mongo_uri)  # Creates global db_service

# Usage throughout the app
db = await get_db()  # Fetches global instance
```
Always call `await get_db()` to access MongoDB; the connection is established during app startup via the lifespan context manager.

### JSON Serialization
MongoDB ObjectIds and datetimes must be serialized for JSON responses. Use `serialize_for_json()` utility in `api/offers.py` before returning response data.

### Jinja2 Template Variables in PDFs
Custom templates use `{{ offer.field }}` syntax. Available fields match the `Offer` model:
```jinja2
{{ offer.product_name }}
{{ offer.brand }}
{{ offer.price }}
{{ offer.mrp }}
{{ offer.valid_till }}
{{ offer.offer_type }}
{{ offer.offer_details }}
{{ offer.custom_fields.any_key }}  <!-- For extensibility -->
```

### Error Handling Convention
- Return HTTPException for API errors with appropriate status codes
- Log errors with `print(f"✗ Error message: {e}")` and `print(f"✓ Success message")`
- Validation failures use Pydantic's built-in error messages

### Frontend State Management
Components use **local React state** (useState) rather than global state management. API calls via `src/services/api.js` Axios instance handle all backend communication.

## Integration Points & Dependencies

### External Libraries
- **Pyppeteer**: Headless Chromium wrapper for HTML→PDF conversion. Requires Node.js + Puppeteer npm package
- **Motor**: Async MongoDB driver. All DB operations are async/await
- **Jinja2**: Server-side template rendering for PDF generation

### File Structure for Custom Templates
Users upload ZIP files with this structure:
```
custom-template.zip/
├── index.html          (required, Jinja2 syntax allowed)
├── styles.css          (optional)
└── assets/             (optional: images, fonts)
```
Extracted to `uploads/templates/{template_id}/` directory.

### Preset Templates
Located in `aops/backend/app/templates/`:
- `preset_minimal.py`: 4-column grid layout (24 offers per A4 page)
- `preset_promo.py`: Eye-catching promotional design
- `preset_multi.py`: 2-column detailed layout

Each file exports `PRESET_*_HTML` string that's stored in MongoDB on app startup.

## Key Files by Purpose

| Purpose | Files |
|---------|-------|
| **Async DB operations** | `app/services/db.py` (DatabaseService class) |
| **PDF rendering logic** | `app/services/pdfgen.py` (PDFGeneratorService class) |
| **API endpoints** | `app/api/{offers,templates,pdf}.py` |
| **Request validation** | `app/models/{offer,template}.py` (Pydantic models) |
| **Frontend API calls** | `src/services/api.js` (Axios instance + helper functions) |
| **Upload workflow** | `src/components/UploadCSV.jsx` |
| **PDF generation UI** | `src/components/PDFGenerator.jsx` |

## Important Constraints & Patterns

- **Async/await required**: All DB and file operations use `async def`. Use `await` when calling database methods
- **Pagination built-in**: `GET /offers` uses skip/limit; frontend handles pagination UI
- **Preset templates immutable**: Once created on startup, they're read-only (no update/delete endpoints)
- **CSV validation strict**: Invalid rows are skipped with a log warning; only rows passing Pydantic validation are inserted
- **PDF output directory**: `./uploads/pdfs/` (created automatically); download via `/downloads/pdfs/{filename}`

## Notable Quirks & Design Decisions

1. **Global service instances**: `db_service`, `pdf_service`, `storage_service` are module-level singletons, not dependency-injected. This avoids passing connections through every function.
2. **HTML in database**: Template HTML is stored directly in MongoDB `templates.html_content` field for quick rendering, avoiding file I/O during PDF generation
3. **Pyppeteer browser persistence**: A new browser instance launches per PDF generation (not reused). This ensures isolation but may be slow for bulk operations
4. **Frontend environment variable**: `VITE_API_URL` controls backend URL (defaults to localhost:8000); used in dev and production
5. **Preset templates auto-init**: On every app startup, `initialize_preset_templates()` checks if presets exist; if not, creates them. Idempotent design.
