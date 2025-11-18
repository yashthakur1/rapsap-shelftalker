#!/usr/bin/env python
"""
Quick preview test for shelf talker loyal template
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'aops', 'backend'))

from app.services.db import init_db, get_db
from app.services.pdfgen import init_pdf_service, get_pdf_service


async def test_loyal_preview():
    mongo_uri = "mongodb://localhost:27017"
    db = await init_db(mongo_uri)
    pdf_service = init_pdf_service(output_dir="./aops/backend/uploads/pdfs")

    templates = await db.get_preset_templates()
    loyal = None
    for t in templates:
        if t.get('name') == 'Shelf Talker - Loyal':
            loyal = t
            break

    if not loyal:
        print('Loyal template not found, creating a quick instance')
        # instantiate from local template definition if not found
        from app.templates.preset_shelf_talker_loyal import PRESET_SHELF_TALKER_LOYAL
        loyal = PRESET_SHELF_TALKER_LOYAL

    # Prepare an offer
    offers = await db.get_offers(skip=0, limit=1)
    if not offers:
        offer = {
            'product_name': 'Lay\'s American Style Cream And Onion Potato Chips',
            'brand': 'Lays',
            'price': 16,
            'mrp': 20,
            'valid_till': '2025-12-31',
            'offer_type': 'Discount',
            'offer_details': 'Buy 1 Get 1'
        }
    else:
        offer = offers[0]

    # custom layout
    layout_options = {"pageSize": {"width": "95mm", "height": "40mm"}}
    page_size_info = pdf_service._resolve_page_size(layout_options.get('pageSize'))
    context = {
        "offers": [offer],
        "layout": layout_options,
        "total_offers": 1,
        "page_size_css": page_size_info['css'],
        "label_width": page_size_info['label_width'],
        "label_height": page_size_info['label_height']
    }

    template_html = loyal.get('html_content')
    rendered = pdf_service.render_template(template_html, context)
    print('--- Rendered HTML Snippet ---')
    print(rendered[:800])
    print('----------- Checks ------------')
    css_size_check = ("@page" in rendered and str(page_size_info['css']) in rendered)
    label_width_check = str(page_size_info['label_width']) in rendered
    label_height_check = str(page_size_info['label_height']) in rendered
    print(f'page_size_css present: {css_size_check}')
    print(f'label_width present: {label_width_check}')
    print(f'label_height present: {label_height_check}')

    await db.disconnect()


if __name__ == '__main__':
    asyncio.run(test_loyal_preview())
