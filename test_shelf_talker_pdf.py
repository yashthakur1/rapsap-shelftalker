#!/usr/bin/env python
"""
Test script to verify shelf talker PDF generation
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'aops', 'backend'))

from app.services.db import init_db, get_db
from app.services.pdfgen import init_pdf_service, get_pdf_service


async def test_shelf_talker_generation():
    """Test generating PDFs for shelf talkers"""
    
    print("=" * 60)
    print("Testing Shelf Talker PDF Generation")
    print("=" * 60)
    
    # Initialize services
    mongo_uri = "mongodb://localhost:27017"
    db = await init_db(mongo_uri)
    pdf_service = init_pdf_service(output_dir="./aops/backend/uploads/pdfs")
    
    print("\n✓ Services initialized")
    
    # Get offers
    offers = await db.get_offers(skip=0, limit=3)
    print(f"✓ Found {len(offers)} offers in database")
    
    if not offers:
        print("\n⚠ No offers found. Please upload some offers first.")
        return
    
    # Get shelf talker templates
    templates = await db.get_preset_templates()
    shelf_talkers = [t for t in templates if "Shelf Talker" in t.get("name", "")]
    
    print(f"✓ Found {len(shelf_talkers)} shelf talker templates")
    
    for template in shelf_talkers:
        template_name = template.get("name", "Unknown")
        print(f"\n📄 Testing: {template_name}")
        print("-" * 60)
        
        # Generate PDF for first offer
        test_offer = offers[0]
        print(f"   Product: {test_offer.get('product_name')}")
        print(f"   Brand: {test_offer.get('brand')}")
        print(f"   Price: ₹{test_offer.get('price')} (MRP: ₹{test_offer.get('mrp')})")
        
        layout_options = template.get("layout_options", {})
        page_size = layout_options.get("pageSize", "A4")
        print(f"   Page Size: {page_size}")
        
        template_html = template.get("html_content", "")
        output_filename = f"test_{template_name.lower().replace(' ', '_').replace('-', '_')}.pdf"
        
        try:
            pdf_path = await pdf_service.generate_batch_pdf(
                offers=[test_offer],
                template_html=template_html,
                layout_options=layout_options,
                output_filename=output_filename
            )
            
            # Check file size
            file_size = os.path.getsize(pdf_path)
            print(f"   ✓ PDF generated: {pdf_path}")
            print(f"   ✓ File size: {file_size:,} bytes ({file_size / 1024:.2f} KB)")
            
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    # Disconnect
    await db.disconnect()
    print("\n" + "=" * 60)
    print("✓ Test completed")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_shelf_talker_generation())
