"""
Preset Template: Minimal Shelf Talker
Landscape format for retail shelf labels (9.5cm x 4cm)
Clean, high-contrast design focusing on savings message
"""

PRESET_SHELF_TALKER_MINIMAL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Minimal Shelf Talkers</title>
    <style>
        @page {
            size: A4;
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
            gap: 10mm;
            justify-content: flex-start;
            align-items: center;
        }

        .shelf-talker {
            width: {{ label_width }};
            height: {{ label_height }};
            box-sizing: border-box;
            border: 3mm solid #000;
            padding: 2mm 4mm;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            background: #fff;
            page-break-inside: avoid;
            break-inside: avoid;
            overflow: hidden;
        }

        .product-name {
            font-size: 10pt;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            line-height: 1.1;
            color: #000;
            margin-bottom: 1mm;
            max-width: 100%;
            word-wrap: break-word;
        }

        .product-details {
            font-size: 7.5pt;
            color: #333;
            margin-bottom: 2mm;
            text-transform: uppercase;
            letter-spacing: 0.2px;
        }

        .savings-line {
            font-size: 9pt;
            font-weight: 600;
            color: #000;
            margin-bottom: 1mm;
        }

        .save-amount {
            font-size: 16pt;
            font-weight: bold;
            color: #000;
            letter-spacing: 0.3px;
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
        <div class="shelf-talker">
            <div class="product-name">{{ offer.product_name | upper }}</div>
            <div class="product-details">{% if not (branding.logo_url or branding.logo_data) %}{{ offer.brand | upper }} • {% endif %}{{ offer.offer_details | upper }}</div>
            <div class="savings-line">ON MRP ₹{{ offer.mrp | int }}</div>
            <div class="save-amount">
                SAVE <span class="rupee">₹</span> {{ (offer.mrp - offer.price) | int }}/-
            </div>
        </div>
    {% endfor %}
    </div>
</body>
</html>
"""

PRESET_SHELF_TALKER_MINIMAL = {
    "name": "Shelf Talker - Minimal",
    "description": "Clean shelf talker design (4 per A4 page)",
    "html_content": PRESET_SHELF_TALKER_MINIMAL_HTML,
    "is_preset": True,
    "layout_options": {
        "pageSize": "A4",
        "perPage": 4,
        "orientation": "portrait",
        "tagWidth": "95mm",
        "tagHeight": "40mm"
    }
}
