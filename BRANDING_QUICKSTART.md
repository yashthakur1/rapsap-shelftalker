# Branding System - Quick Start Guide

## 🎯 What's New

You can now select different brand configurations (logos, colors, fonts) from a dropdown menu in the Template Manager. The selected brand will automatically apply to your PDF templates during preview and generation.

## 📍 How to Use

### Step 1: Start the Application

```powershell
# Terminal 1 - Backend
cd d:\BitRoot-Project-Grocery
python run_backend.py

# Terminal 2 - Frontend
cd d:\BitRoot-Project-Grocery\aops\frontend
npm run dev
```

### Step 2: Access the Application

Open your browser to: `http://localhost:5173`

### Step 3: Use Branding Dropdown

1. **Upload Offers** (Step 1)
   - Upload your CSV file with offers

2. **Select Offers** (Step 2)
   - Check the offers you want to include in the PDF

3. **Select Template & Branding** (Step 3)
   - Choose a template (Shelf Talker - Loyal or Shelf Talker - Branded recommended)
   - **NEW:** Select a brand from the "Brand Selection" dropdown
   - You'll see:
     - Brand name in dropdown (Loyal / Default)
     - Color preview showing primary brand color
     - Font information (heading font name)
   - Preview updates automatically when you change brand selection

4. **Generate PDF** (Step 4)
   - Click "Generate PDF"
   - Your PDF will be created with the selected brand logo, colors, and fonts

## 🎨 Available Brands

### Loyal Brand
- **Logo:** White "loyal" text (SVG)
- **Primary Color:** #5074F3 (Blueberry Blue)
- **Accent Color:** #2F448D (Deep Blue)
- **Fonts:** Barlow Condensed (headings), DM Sans (body)

### Default Brand
- **Logo:** None (uses text fallback)
- **Primary Color:** #5074F3
- **Accent Color:** #2F448D
- **Fonts:** Arial, Helvetica (system fonts)

## 🖼️ Where Branding Appears

The selected brand affects:
- **Logo:** Displays brand logo in template (or brand text if no logo)
- **Colors:** 
  - Background gradients (blue accent band)
  - Brand section background
- **Typography:**
  - Product names (body font)
  - Prices and percentages (heading font)
  - Labels and badges

## 🧪 Testing the Feature

### Quick Test:

1. Make sure you have offers in the database:
   ```powershell
   python -c "from sample_offers import create_sample_offers; create_sample_offers()"
   ```

2. Open the app and select "Shelf Talker - Loyal" template

3. Try switching between "Loyal" and "Default" brands in the dropdown

4. Watch the preview update with different brand styling

5. Generate a PDF to see the final result

### Preview Test Script:

You can also test the backend directly:

```powershell
python test_branding.py
```

This will:
- Check if /branding endpoint works
- Test preview with branding applied
- Verify logo, colors, and fonts are rendered

## 📝 Adding New Brands

To add a new brand, edit `aops/backend/app/config/branding.py`:

```python
BRAND_CONFIGS = {
    "loyal": { ... },
    "default": { ... },
    "your_brand": {  # NEW BRAND
        "name": "Your Brand Name",
        "logo_url": "/logos/your_logo.svg",
        "colors": {
            "primary": "#FF5733",
            "accent": "#C70039",
            "text": "#000000",
            "textLight": "#FFFFFF",
            "background": "#FFFFFF",
            "backgroundGray": "#F5F5F5"
        },
        "fonts": {
            "heading": "'Montserrat', Arial, sans-serif",
            "body": "'Open Sans', Arial, sans-serif"
        }
    }
}
```

Then add your logo file to: `aops/backend/app/logos/your_logo.svg`

Restart the backend server, and your new brand will appear in the dropdown!

## 🐛 Troubleshooting

### Branding dropdown not showing
- Make sure backend is running on http://localhost:8000
- Check browser console for fetch errors
- Verify `/branding` endpoint returns data: http://localhost:8000/branding

### Logo not displaying
- Check that logo file exists in `aops/backend/app/logos/`
- Verify logo URL in branding config starts with `/logos/`
- Check that `/logos` static mount is working: http://localhost:8000/logos/loyal.svg

### Colors not applying
- Inspect HTML preview to see if color variables are present
- Check template uses `{{ branding.colors.primary }}` syntax
- Verify branding is passed in layout_options

### Preview not updating when changing brand
- Check that `selectedBrand` state is updating in Dashboard
- Verify TemplateManager receives `selectedBrand` prop
- Ensure useEffect dependency array includes `selectedBrand`

## 🎓 Technical Architecture

```
Frontend                    Backend                     Template
--------                    -------                     --------
User selects brand    →     /branding endpoint    →    BRAND_CONFIGS
    ↓                           ↓
Dashboard state              Returns brand list
    ↓                           ↓
TemplateManager          /pdf/preview accepts     Jinja2 renders
    ↓                    layout_options.branding   {{ branding.* }}
Preview updates              ↓                          ↓
    ↓                    render_template()         Logo, colors, fonts
PDFGenerator            context["branding"]        applied to HTML
    ↓                           ↓                          ↓
/pdf/generate           Pyppeteer renders          Final PDF with
with branding           HTML to PDF                brand styling
```

## 📚 Related Files

- **Config:** `aops/backend/app/config/branding.py`
- **Logos:** `aops/backend/app/logos/*.svg`
- **API:** `aops/backend/app/main.py` (branding endpoint)
- **PDF Service:** `aops/backend/app/services/pdfgen.py`
- **PDF API:** `aops/backend/app/api/pdf.py`
- **Templates:** `aops/backend/app/templates/preset_shelf_talker_*.py`
- **Frontend:** `aops/frontend/src/components/TemplateManager.jsx`
- **Frontend:** `aops/frontend/src/components/PDFGenerator.jsx`
- **Frontend:** `aops/frontend/src/pages/Dashboard.jsx`

---

**Enjoy your new branding system! 🎉**
