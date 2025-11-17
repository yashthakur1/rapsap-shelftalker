# AOPS - Automated Offer Print System

A full-stack web application that automates generating and printing offer tags from CSV files. Supports both preset and custom HTML/CSS templates for PDF generation.

## 🎯 Features

- **CSV Upload**: Batch import offers from CSV files
- **Offer Management**: View and select offers in an intuitive grid
- **Template System**: Choose from preset templates or upload custom designs
- **PDF Generation**: Server-side rendering with Jinja2 templating
- **Responsive Design**: Works seamlessly on all devices
- **Real-time Preview**: See changes instantly
- **Batch Processing**: Generate PDFs for multiple offers at once

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Motor** - Async MongoDB driver
- **Pyppeteer** - Headless browser for PDF generation
- **Pydantic** - Data validation
- **Jinja2** - Template rendering

### Frontend
- **React** 18 - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Utility-first CSS
- **Axios** - HTTP client
- **React Hot Toast** - Notifications

### Database
- **MongoDB** - NoSQL database for offers and templates

## 📁 Project Structure

```
aops/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── offers.py          # Offer endpoints
│   │   │   ├── templates.py        # Template endpoints
│   │   │   └── pdf.py              # PDF generation endpoints
│   │   ├── models/
│   │   │   ├── offer.py            # Offer Pydantic model
│   │   │   └── template.py         # Template Pydantic model
│   │   ├── services/
│   │   │   ├── db.py               # MongoDB operations
│   │   │   ├── pdfgen.py           # PDF generation service
│   │   │   └── storage.py          # File storage service
│   │   ├── templates/
│   │   │   ├── preset_minimal.html # Minimal template
│   │   │   ├── preset_promo.html   # Promotional template
│   │   │   └── preset_multi.html   # Multi-column template
│   │   └── main.py                 # FastAPI app entry point
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadCSV.jsx       # CSV upload component
│   │   │   ├── OfferPreview.jsx    # Offer grid component
│   │   │   ├── TemplateManager.jsx # Template selection
│   │   │   └── PDFGenerator.jsx    # PDF generation
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx       # Main dashboard
│   │   │   └── Settings.jsx        # Settings page
│   │   ├── services/
│   │   │   └── api.js              # API calls
│   │   ├── App.jsx                 # Main app component
│   │   ├── main.jsx                # React entry point
│   │   └── index.css               # Global styles
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
└── README.md
```

## 🚀 Quick Start

### Backend Setup

1. **Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure MongoDB**
```bash
# Default: mongodb://localhost:27017
# Or set env variable: MONGODB_URI=your_mongodb_url
```

3. **Run Server**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at `http://localhost:8000`
API docs available at `http://localhost:8000/docs`

### Frontend Setup

1. **Install Dependencies**
```bash
cd frontend
npm install
```

2. **Start Development Server**
```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

3. **Build for Production**
```bash
npm run build
```

## 📝 API Endpoints

### Offers
- `POST /offers/upload-csv` - Upload CSV file
- `GET /offers?skip=0&limit=50` - Get offers with pagination
- `GET /offers/{offer_id}` - Get single offer

### Templates
- `POST /templates/upload` - Upload custom template ZIP
- `GET /templates` - Get all templates
- `GET /templates/preset` - Get preset templates only
- `GET /templates/{template_id}` - Get single template

### PDF Generation
- `POST /pdf/generate` - Generate PDF with selected offers
- `POST /pdf/preview` - Preview PDF as HTML

## 📊 CSV Format

Expected columns in CSV file:

```csv
product_id,product_name,brand,offer_type,offer_details,price,mrp,valid_till
PRD-001,Wireless Headphones,TechBrand,Discount,20% off,4999,6999,2025-12-31
PRD-002,Smart Watch,TechBrand,Seasonal,Limited Time,7999,9999,2025-12-15
```

## 🎨 Preset Templates

1. **Minimal Clean** - Simple 4-column grid with essential info
2. **Promotional Bold** - Eye-catching design with vibrant colors
3. **Detailed Multi-Column** - 2-column layout with pricing breakdown

## 📦 Custom Templates

Upload a ZIP file containing:
- `index.html` - Main template file with Jinja2 syntax
- `styles.css` (optional) - Additional CSS
- Other assets (images, fonts, etc.)

Use `{{ offer.field }}` in templates to reference offer data:
- `{{ offer.product_name }}`
- `{{ offer.brand }}`
- `{{ offer.price }}`
- `{{ offer.mrp }}`
- `{{ offer.valid_till }}`
- `{{ offer.offer_type }}`
- `{{ offer.offer_details }}`

## 🔧 Environment Variables

### Backend (.env)
```
MONGODB_URI=mongodb://localhost:27017
ENVIRONMENT=development
DEBUG=true
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

## 📚 Usage Workflow

1. **Upload CSV** - Select and upload your offers CSV file
2. **Preview Offers** - View uploaded offers in grid format
3. **Select Offers** - Check which offers to include in PDF
4. **Choose Template** - Select a preset or upload custom template
5. **Generate PDF** - Click to create PDF with selected offers
6. **Download** - Download the generated PDF to print

## 🎯 Key Features Details

### CSV Upload
- Validates data against Pydantic models
- Skips invalid rows and provides feedback
- Shows preview of first 5 uploaded offers
- Returns count of successfully inserted documents

### Offer Grid
- Responsive grid with auto-fill columns
- Checkbox selection for batch operations
- Pagination support for large datasets
- Shows key offer information

### Template System
- Preset templates with professional designs
- Custom template upload via ZIP files
- Live template selection with instant preview
- Layout options (page size, offers per page, orientation)

### PDF Generation
- Server-side rendering using Jinja2
- Async processing with pyppeteer
- Configurable page layout and spacing
- Download links for generated PDFs

## 🐛 Troubleshooting

### MongoDB Connection Issues
```bash
# Ensure MongoDB is running
mongod

# Check connection string in .env
MONGODB_URI=mongodb://localhost:27017
```

### PDF Generation Fails
- Ensure Node.js dependencies are installed
- Check pyppeteer installation
- Verify sufficient disk space for temporary files

### CORS Errors
- Backend CORS is configured for localhost:3000 and localhost:5173
- Add additional origins in `app/main.py` if needed

### Missing Preset Templates
- Preset templates are auto-initialized on server startup
- Check database connection and permissions

## 🚢 Production Deployment

1. **Build Frontend**
```bash
cd frontend
npm run build
```

2. **Set Environment Variables**
```bash
ENVIRONMENT=production
MONGODB_URI=your_production_mongodb
FRONTEND_URL=your_frontend_url
```

3. **Run Backend**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

4. **Serve Frontend**
- Deploy `frontend/dist` to static file server
- Or use FastAPI static file serving

## 📄 License

MIT

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**AOPS** - Making offer tag printing automated and effortless! 🏷️
