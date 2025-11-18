"""
Preset Template: Loyal Shelf Talker
A variant with brand accent and large price area in right section.
"""

PRESET_SHELF_TALKER_LOYAL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Loyal Shelf Talker</title>
    <style>
        @page { size: {{ page_size_css }}; margin: 0; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body { width: 100%; min-height: 100%; margin: 0; padding: 0; }
        body { font-family: 'DM Sans', 'Arial', sans-serif; background: #fff; color: #030303; }
        .shelf-wrapper { width: {{ label_width }}; height: {{ label_height }}; position: relative; overflow: hidden; background: white; }

        /* brand logo */
        .brand-logo { position: absolute; left: 12px; top: calc(12mm + 42px); width: 120px; margin-top:-15px; height: 60px; object-fit: contain; }

        /* left area (product details) */
        .product-name { position: absolute; left: 12px; top: 12px; color: #030303; font-size: 14px; font-family: {{ branding.fonts.body if branding.fonts else "'DM Sans'" }}, Arial, sans-serif; font-weight: 500; line-height: 16.8px; max-width: calc(60% - 12px); word-wrap: break-word; }

        /* price area on right */
        .rupee-symbol { position: absolute; left: calc(60% + 12px); top: 35px; color: #030303; font-size: 32px; font-family: {{ branding.fonts.heading if branding.fonts else "'Barlow Condensed'" }}, Arial, sans-serif; font-style: italic; font-weight: 500; text-transform: uppercase; }
        .price-major { position: absolute; left: calc(60% + 30px); top: 12px; color: #030303; font-size: 64px; font-family: {{ branding.fonts.heading if branding.fonts else "'Barlow Condensed'" }}, Arial, sans-serif; font-style: italic; font-weight: 600; text-transform: uppercase; }

        /* accent blue band */
        .blue-band { position: absolute; left: 0; top: calc(12mm + 40px); width: calc(100%); height: 9mm; background: linear-gradient(180deg, {{ branding.colors.primary if branding.colors else "#5074F3" }} 0%, {{ branding.colors.accent if branding.colors else "#2F448D" }} 100%); }

        /* brand badge */
        .brand-badge { position: absolute; left: 12px; top: calc(12mm + 48px); color: #fff; font-size: 22.48px; font-family: {{ branding.fonts.heading if branding.fonts else "'Barlow Condensed'" }}, Arial, sans-serif; font-style: italic; font-weight: 600; line-height: 17.98px; }

        /* offer percent */
        .percent { position: absolute; left: calc(60% + 16px); top: calc(12mm + 50px); color: #fff; display: flex; gap: 4px; align-items: center; font-family: {{ branding.fonts.heading if branding.fonts else "'Barlow Condensed'" }}, Arial, sans-serif; }
        .percent .value { font-size: 20px; font-weight: 700; text-transform: uppercase; }
        .percent .label { font-size: 13px; font-weight: 700; line-height: 11.7px; }

        /* small rupee font for price */
        .rupee { font-family: {{ branding.fonts.heading if branding.fonts else "'Barlow Condensed'" }}, Arial, sans-serif; }
    </style>
</head>
<body>
    {% for offer in offers %}
    <div class="shelf-wrapper">
        <div class="product-name">{{ offer.product_name | default('') }}</div>
        <div class="rupee-symbol">₹</div>
        <div class="price-major">{{ offer.price | int }}</div>
        <div class="blue-band"></div>
        {% if branding.logo_url %}
        {% if 'svg' in (branding.logo_url | lower) %}
        <img src="{{ branding.logo_url }}" alt="Brand Logo" class="brand-logo" style="filter: brightness(0) invert(1);" />
        {% else %}
        <img src="{{ branding.logo_url }}" alt="Brand Logo" class="brand-logo" />
        {% endif %}
        {% else %}
        <div class="brand-badge">{{ offer.brand|upper if offer.brand else 'LOYAL' }}</div>
        {% endif %}
        {% if offer.mrp and offer.price %}
        <div class="percent">
            <div class="value">{{ ((offer.mrp - offer.price) / offer.mrp * 100) | int }}%</div>
            <div class="label">Additional savings</div>
        </div>
        {% endif %}
    </div>
    {% endfor %}
</body>
</html>
"""

PRESET_SHELF_TALKER_LOYAL = {
    "name": "Shelf Talker - Loyal",
    "description": "Compact, branded shelf talker with large price and blue accent bar",
    "html_content": PRESET_SHELF_TALKER_LOYAL_HTML,
    "is_preset": True,
    "layout_options": {
        "pageSize": {"width": "95mm", "height": "40mm"},
        "perPage": 1,
        "orientation": "landscape"
    }
}
