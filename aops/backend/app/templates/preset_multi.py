"""
Preset template: Multi-column detailed design.
Shows more information per tag with better pricing breakdown.
"""

PRESET_MULTI_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Detailed Offer Tags</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f9f9f9;
            padding: 10mm;
        }
        
        .page {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            background: white;
            padding: 10mm;
            page-break-after: always;
        }
        
        .offer-tag {
            border: 2px solid #3E6FF4;
            border-radius: 10px;
            padding: 14px;
            background: linear-gradient(135deg, #f5f5ff 0%, #e8eeff 100%);
            break-inside: avoid;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 160px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .header {
            border-bottom: 2px solid #3E6FF4;
            padding-bottom: 8px;
            margin-bottom: 8px;
        }
        
        .product-name {
            font-weight: bold;
            font-size: 12px;
            color: #333;
            margin-bottom: 2px;
            word-break: break-word;
        }
        
        .brand {
            font-size: 10px;
            color: #666;
            margin-bottom: 4px;
        }
        
        .offer-badge {
            display: inline-block;
            background: #FFD84D;
            color: #333;
            padding: 3px 6px;
            border-radius: 3px;
            font-weight: bold;
            font-size: 9px;
        }
        
        .content {
            margin: 8px 0;
        }
        
        .offer-details {
            font-size: 10px;
            color: #333;
            margin: 4px 0;
            line-height: 1.4;
        }
        
        .price-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
            margin: 8px 0;
        }
        
        .price-item {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .price-label {
            font-size: 8px;
            color: #666;
            margin-bottom: 2px;
        }
        
        .price-value {
            font-size: 14px;
            font-weight: bold;
            color: #3E6FF4;
        }
        
        .mrp-value {
            font-size: 10px;
            color: #999;
            text-decoration: line-through;
        }
        
        .footer {
            border-top: 1px solid #ddd;
            padding-top: 6px;
            margin-top: 6px;
            text-align: center;
        }
        
        .valid-till {
            font-size: 9px;
            color: #d32f2f;
            font-weight: bold;
        }
        
        @media print {
            body {
                background: white;
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
            <div class="header">
                <div class="product-name">{{ offer.product_name }}</div>
                <div class="brand">{{ offer.brand }}</div>
                <span class="offer-badge">{{ offer.offer_type }}</span>
            </div>
            
            <div class="content">
                <div class="offer-details">{{ offer.offer_details }}</div>
                
                <div class="price-grid">
                    <div class="price-item">
                        <div class="price-label">Sale Price</div>
                        <div class="price-value">₹{{ offer.price }}</div>
                    </div>
                    <div class="price-item">
                        <div class="price-label">MRP</div>
                        {% if offer.mrp %}
                            <div class="mrp-value">₹{{ offer.mrp }}</div>
                        {% else %}
                            <div class="mrp-value">-</div>
                        {% endif %}
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <div class="valid-till">✓ Valid Till: {{ offer.valid_till }}</div>
            </div>
        </div>
        
        {% if loop.last or loop.index0 % 23 == 23 %}
            </div>
        {% endif %}
    {% endfor %}
</body>
</html>
"""
