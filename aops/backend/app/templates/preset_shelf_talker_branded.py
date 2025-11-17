"""
Preset Template: Branded Shelf Talker
Landscape format for retail shelf labels (9.5cm x 4cm)
Modern design with brand accent and discount percentage
"""

PRESET_SHELF_TALKER_BRANDED_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Branded Shelf Talkers</title>
    <style>
        @page {
            size: {{ page_size_css }};
            margin: 0;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html,
        body {
            width: 100%;
            min-height: 100%;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Arial', 'Helvetica', sans-serif;
            background: #ffffff;
            color: #111;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding: 12mm 10mm 10mm;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }

        .page-layout {
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 4mm;
            justify-content: center;
            align-items: center;
        }

        .shelf-wrapper {
            width: {{ label_width }};
            height: {{ label_height }};
            box-sizing: border-box;
            border: 0;
            overflow: hidden;
            page-break-after: always;
            break-inside: avoid;
            display: flex;
            background: #fff;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        }

        .left-section {
            flex: 0 0 66%;
            background: white;
            padding: 3mm 4mm;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 1mm;
        }

        .brand-section {
            flex: 0 0 34%;
            background: #0033cc;
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2mm;
            text-align: center;
        }

        .product-name {
            font-size: 8.5pt;
            color: #333;
            line-height: 1.1;
            font-weight: 500;
        }

        .product-details {
            font-size: 7pt;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.2px;
        }

        .price-row {
            display: flex;
            flex-direction: column;
            gap: 0.5mm;
            margin-top: 2mm;
        }

        .price-main {
            font-size: 18pt;
            font-weight: bold;
            color: #000;
            letter-spacing: -0.5px;
            line-height: 1;
        }

        .price-label {
            font-size: 6.5pt;
            color: #666;
            text-transform: uppercase;
        }

        .brand-logo {
            font-size: 12pt;
            font-weight: bold;
            letter-spacing: 0.5px;
            font-style: italic;
            text-transform: uppercase;
        }

        .discount-badge {
            font-size: 15pt;
            font-weight: bold;
            line-height: 1;
        }

        .discount-label {
            font-size: 6.5pt;
            line-height: 1.2;
            text-transform: uppercase;
            letter-spacing: 0.2px;
        }

        .rupee {
            font-family: 'Arial', sans-serif;
        }

        @media print {
            body {
                padding: 0;
            }

            .page-layout {
                gap: 2mm;
            }
        }
    </style>
</head>
<body>
    <div class="page-layout">
        {% for offer in offers %}
        <div class="shelf-wrapper">
            <div class="left-section">
                <div class="product-name">{{ offer.product_name }}</div>
                <div class="product-details">{{ offer.brand }} {{ offer.offer_details }}</div>
                <div class="price-row">
                    <div class="price-main"><span class="rupee">₹</span>{{ (offer.mrp - offer.price)|int }}<sup style="font-size:9pt">OFF</sup></div>
                    <div class="price-label">ON MRP</div>
                </div>
            </div>
            <div class="brand-section">
                <div class="brand-logo">{{ (offer.brand|upper) if offer.brand else 'LOYAL' }}</div>
                {% if offer.mrp and offer.price %}
                <div class="discount-badge">{{ ((offer.mrp - offer.price) / offer.mrp * 100)|int }}%</div>
                <div class="discount-label">additional savings</div>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

PRESET_SHELF_TALKER_BRANDED = {
    "name": "Shelf Talker - Branded",
    "description": "Modern shelf talker with brand accent bar (9.5cm x 4cm, landscape)",
    "html_content": PRESET_SHELF_TALKER_BRANDED_HTML,
    "is_preset": True,
    "layout_options": {
        "pageSize": {"width": "95mm", "height": "40mm"},
        "perPage": 1,
        "orientation": "landscape"
    }
}
