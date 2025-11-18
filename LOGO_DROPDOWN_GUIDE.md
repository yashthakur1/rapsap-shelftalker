# Quick Start Guide - Using All 4 Logos

## 🚀 How to Use the New Logo Dropdown

### Step 1: Start the Application

Open two terminal windows:

**Terminal 1 - Backend:**
```bash
cd d:\BitRoot-Project-Grocery
python run_backend.py
```
Wait for: `✓ All services initialized successfully`

**Terminal 2 - Frontend:**
```bash
cd d:\BitRoot-Project-Grocery\aops\frontend
npm run dev
```
Wait for: `Local: http://localhost:5173/`

### Step 2: Open the Application

Open your browser and go to: **http://localhost:5173**

### Step 3: Navigate to Template Manager

1. **Upload CSV** (Step 1)
   - Click "Choose File" and upload your offers CSV
   - Or use sample data if already uploaded

2. **Select Offers** (Step 2)
   - Check the checkboxes for offers you want in your PDF

3. **Select Template & Brand** (Step 3)
   - Choose a template (e.g., "Shelf Talker - Loyal")
   - **Look for the "Brand Selection" dropdown** 👇

### Step 4: Use the Brand Selection Dropdown

You'll see a dropdown with 5 options:

1. **Loyal** - Original white text SVG logo
2. **Frame 27** - PNG logo image
3. **Logo W** - White logo PNG
4. **Symbol Logo B** - Symbol-based logo PNG
5. **Default (No Logo)** - No logo, uses text fallback

### Step 5: See the Logo Preview

When you select a brand, you'll see:

📸 **Logo Preview Card:**
- Logo displayed on gradient background (using brand colors)
- The logo appears in white for visibility

🎨 **Color Information:**
- Primary Color: Blue circle + hex code (e.g., #5074F3)
- Accent Color: Darker blue circle + hex code (e.g., #2F448D)

🔤 **Font Information:**
- Heading Font: Barlow Condensed
- Body Font: DM Sans

### Step 6: Preview Updates Automatically

- The template preview below will update with your selected logo
- You'll see the logo appear in the shelf talker template
- Colors and fonts will match the selected brand

### Step 7: Generate PDF

Click **"Generate PDF"** button:
- Your PDF will be created with the selected logo
- The logo will appear on all offers in the batch
- Brand colors and fonts will be applied

### Step 8: Download

Click **"Download PDF"** to save your branded PDF!

---

## 🎯 What Each Logo Looks Like

### Loyal
- **Style:** Clean text-based logo
- **Format:** SVG (vector)
- **Best for:** Professional, minimalist designs

### Frame 27
- **Style:** Framed logo design
- **Format:** PNG (raster image)
- **Best for:** Boxed or contained layouts

### Logo W
- **Style:** White logo variant
- **Format:** PNG (raster image)
- **Best for:** Dark or colored backgrounds

### Symbol Logo B
- **Style:** Symbol-based brand mark
- **Format:** PNG (raster image)
- **Best for:** Icon/symbol-focused designs

### Default (No Logo)
- **Style:** No logo image
- **Format:** Text fallback (uses brand name)
- **Best for:** Testing or text-only designs

---

## 🧪 Testing All Logos

### Quick Visual Test:
1. Select "Shelf Talker - Loyal" template
2. Check one offer
3. Try each brand in the dropdown:
   - Select "Loyal" → See logo preview
   - Select "Frame 27" → Logo changes
   - Select "Logo W" → Logo changes
   - Select "Symbol Logo B" → Logo changes
   - Select "Default" → No logo shown
4. Watch the preview update for each selection

### Automated Test:
```bash
python test_all_logos.py
```

This will check:
- ✓ All 5 brands are available
- ✓ Logo files are accessible
- ✓ File sizes and formats are correct

---

## ❓ Troubleshooting

### Logo not showing in dropdown preview?
- Check that backend is running (http://localhost:8000)
- Verify logo files exist in `aops/backend/app/logos/`
- Check browser console for errors
- Try refreshing the page (Ctrl + R)

### Logo shows broken image icon?
- Verify the logo file path is correct
- Check that `/logos` route is mounted in backend
- Test logo URL directly: http://localhost:8000/logos/Frame%2027.png

### Logo not appearing in PDF?
- Make sure you selected a brand before generating
- Check that the template supports branding (Shelf Talker templates do)
- Verify branding is being passed in the API request (check Network tab)

### Dropdown is empty?
- Backend might not be running
- Check `/branding` endpoint: http://localhost:8000/branding
- Look for errors in backend terminal

### Logo appears too large/small?
- Logo size is auto-scaled to max-height: 48px in preview
- In PDF, logo size depends on template CSS
- Edit template files to adjust logo size if needed

---

## 🎨 Customizing Brand Colors

To change brand colors, edit `aops/backend/app/config/branding.py`:

```python
"loyal": {
    "colors": {
        "primary": "#5074F3",    # ← Change this
        "accent": "#2F448D",     # ← Change this
        # ...
    }
}
```

Then restart the backend for changes to take effect.

---

## 📸 Expected Appearance

### Dropdown (Closed):
```
┌─────────────────────────────┐
│ Brand Selection:      ▼     │
│ ┌─────────────────────────┐ │
│ │ Loyal              ▼    │ │
│ └─────────────────────────┘ │
└─────────────────────────────┘
```

### Dropdown (Open):
```
┌─────────────────────────────┐
│ Loyal                       │
│ Frame 27                    │
│ Logo W                      │
│ Symbol Logo B               │
│ Default (No Logo)           │
└─────────────────────────────┘
```

### Preview Card (After Selection):
```
┌─────────────────────────────┐
│ Logo Preview:               │
│ ┌─────────────────────────┐ │
│ │   [LOGO IMAGE]          │ │ ← On blue gradient
│ └─────────────────────────┘ │
│                             │
│ Primary: ● #5074F3          │
│ Accent:  ● #2F448D          │
│                             │
│ Fonts:                      │
│   Heading: Barlow Condensed │
│   Body: DM Sans             │
└─────────────────────────────┘
```

---

**Enjoy your multi-logo branding system! 🎉**

Need help? Check:
- `ALL_LOGOS_INTEGRATION.md` for technical details
- `BRANDING_QUICKSTART.md` for general branding guide
- `BRANDING_IMPLEMENTATION.md` for implementation docs
