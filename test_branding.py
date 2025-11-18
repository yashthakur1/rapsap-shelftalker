"""
Test script to verify branding system is working correctly
Tests:
1. Branding API endpoint returns available brands
2. Preview endpoint accepts branding in layout_options
3. Template renders with branding variables (logo, colors, fonts)
"""

import asyncio
import aiohttp
import json

API_BASE = "http://localhost:8000"

async def test_branding_api():
    """Test GET /branding endpoint"""
    print("=" * 60)
    print("TEST 1: Branding API Endpoint")
    print("=" * 60)
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE}/branding") as response:
            if response.status == 200:
                data = await response.json()
                print(f"✓ Status: {response.status}")
                print(f"✓ Available brands: {len(data.get('brands', []))}")
                for brand in data.get('brands', []):
                    print(f"  - {brand['name']} (ID: {brand['id']})")
                    print(f"    Logo: {brand.get('logo_url', 'N/A')}")
                    print(f"    Primary Color: {brand.get('colors', {}).get('primary', 'N/A')}")
                    print(f"    Heading Font: {brand.get('fonts', {}).get('heading', 'N/A')}")
                return data
            else:
                print(f"✗ Failed: Status {response.status}")
                text = await response.text()
                print(f"  Response: {text}")
                return None

async def test_preview_with_branding():
    """Test preview endpoint with branding in layout_options"""
    print("\n" + "=" * 60)
    print("TEST 2: Preview with Branding")
    print("=" * 60)
    
    async with aiohttp.ClientSession() as session:
        # First get branding config
        async with session.get(f"{API_BASE}/branding") as response:
            branding_data = await response.json()
            loyal_brand = next((b for b in branding_data.get('brands', []) if b['id'] == 'loyal'), None)
        
        if not loyal_brand:
            print("✗ Loyal brand not found")
            return None
        
        # Get first offer ID
        async with session.get(f"{API_BASE}/offers?limit=1") as response:
            offers_data = await response.json()
            if not offers_data.get('offers'):
                print("✗ No offers found - upload sample CSV first")
                return None
            first_offer_id = offers_data['offers'][0]['id']
        
        # Get templates
        async with session.get(f"{API_BASE}/templates") as response:
            templates_data = await response.json()
            loyal_template = next((t for t in templates_data.get('templates', []) 
                                  if 'Loyal' in t.get('name', '')), None)
        
        if not loyal_template:
            print("✗ Loyal template not found")
            return None
        
        template_id = loyal_template.get('id') or loyal_template.get('_id')
        print(f"Using template: {loyal_template['name']} (ID: {template_id})")
        print(f"Using brand: {loyal_brand['name']}")
        
        # Preview with branding
        payload = {
            "offer_ids": [first_offer_id],
            "template_id": template_id,
            "layout_options": {
                "pageSize": {"width": "95mm", "height": "40mm"},
                "perPage": 1,
                "branding": loyal_brand
            }
        }
        
        async with session.post(
            f"{API_BASE}/pdf/preview",
            json=payload,
            headers={"Content-Type": "application/json"}
        ) as response:
            if response.status == 200:
                data = await response.json()
                html = data.get('html_preview', '')
                print(f"✓ Status: {response.status}")
                print(f"✓ HTML Length: {len(html)} chars")
                
                # Check if branding variables are present
                checks = {
                    "Logo URL": loyal_brand['logo_url'] in html,
                    "Primary Color": loyal_brand['colors']['primary'] in html,
                    "Heading Font": "Barlow Condensed" in html,
                    "Body Font": "DM Sans" in html,
                }
                
                print("\nBranding Variables Check:")
                for name, present in checks.items():
                    status = "✓" if present else "✗"
                    print(f"  {status} {name}: {'Present' if present else 'Missing'}")
                
                return html
            else:
                print(f"✗ Failed: Status {response.status}")
                text = await response.text()
                print(f"  Response: {text}")
                return None

async def main():
    print("\n🧪 BRANDING SYSTEM TEST SUITE\n")
    
    # Test 1: Branding API
    brands = await test_branding_api()
    
    # Test 2: Preview with branding
    if brands:
        html = await test_preview_with_branding()
    
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETE")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
