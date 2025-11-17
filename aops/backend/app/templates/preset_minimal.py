"""
Preset template: Minimal clean offer tag.
Simple, modern design for A4 with 24 tags per page.
"""

PRESET_MINIMAL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Offer Tags</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 10mm;
        }
        
        .page {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            background: white;
            padding: 10mm;
            page-break-after: always;
        }
        
        .offer-tag {
            border: 2px solid #3E6FF4;
            border-radius: 8px;
            padding: 12px;
            background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%);
            text-align: center;
            break-inside: avoid;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 120px;
        }
        
        .product-name {
            font-weight: bold;
            font-size: 11px;
            color: #333;
            margin-bottom: 6px;
            word-break: break-word;
        }
        
        .brand {
            font-size: 9px;
            color: #666;
            margin-bottom: 4px;
        }
        
        .offer-badge {
            background: #FFD84D;
            color: #333;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 10px;
            margin: 4px 0;
        }
        
        .price-section {
            margin-top: 6px;
        }
        
        .price {
            font-size: 14px;
            font-weight: bold;
            color: #3E6FF4;
            margin: 2px 0;
        }
        
        .mrp {
            font-size: 9px;
            color: #999;
            text-decoration: line-through;
        }
        
        .valid-till {
            font-size: 8px;
            color: #d32f2f;
            margin-top: 4px;
        }
        
        @media print {
            body {
                background: white;
            }
            .page {
                page-break-after: always;
            }
        }
    </style>
</head>
<body>
    {% for offer in offers %}
        {% if loop.first or loop.index0 % 24 == 0 %}
            <div class="page">
        {% endif %}
        
        <div class="offer-tag">
            <div>
                <div class="product-name">{{ offer.product_name }}</div>
                <div class="brand">{{ offer.brand }}</div>
                <div class="offer-badge">{{ offer.offer_type }}</div>
            </div>
            <div class="price-section">
                <div class="price">₹{{ offer.price }}</div>
                {% if offer.mrp %}
                    <div class="mrp">MRP: ₹{{ offer.mrp }}</div>
                {% endif %}
                <div class="valid-till">Valid: {{ offer.valid_till }}</div>
            </div>
        </div>
        
        {% if loop.last or loop.index0 % 23 == 23 %}
            </div>
        {% endif %}
    {% endfor %}
</body>
</html>
"""
