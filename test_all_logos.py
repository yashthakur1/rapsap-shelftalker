"""
Quick test to verify all 4 logos are available in branding API
"""

import asyncio
import aiohttp
import json

async def test_branding_logos():
    print("=" * 60)
    print("Testing Branding API - All Logos")
    print("=" * 60)
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("http://localhost:8000/branding") as response:
                if response.status == 200:
                    data = await response.json()
                    brands = data.get('brands', [])
                    
                    print(f"\n✓ Status: {response.status}")
                    print(f"✓ Total brands: {len(brands)}\n")
                    
                    for i, brand in enumerate(brands, 1):
                        print(f"{i}. {brand['name']}")
                        print(f"   ID: {brand['id']}")
                        print(f"   Logo: {brand.get('logo_url', 'None')}")
                        print(f"   Primary Color: {brand['colors']['primary']}")
                        print(f"   Accent Color: {brand['colors']['accent']}")
                        print(f"   Heading Font: {brand['fonts']['heading'][:30]}...")
                        print()
                    
                    # Verify logo files exist
                    print("Checking logo file accessibility:")
                    for brand in brands:
                        if brand.get('logo_url'):
                            logo_url = f"http://localhost:8000{brand['logo_url']}"
                            try:
                                async with session.get(logo_url) as logo_resp:
                                    if logo_resp.status == 200:
                                        content_type = logo_resp.headers.get('Content-Type', '')
                                        size = len(await logo_resp.read())
                                        print(f"  ✓ {brand['name']}: {content_type} ({size} bytes)")
                                    else:
                                        print(f"  ✗ {brand['name']}: Status {logo_resp.status}")
                            except Exception as e:
                                print(f"  ✗ {brand['name']}: {str(e)}")
                    
                    print("\n" + "=" * 60)
                    print("✅ All brands loaded successfully!")
                    print("=" * 60)
                    
                else:
                    print(f"✗ Failed: Status {response.status}")
                    text = await response.text()
                    print(f"Response: {text}")
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            print("\nMake sure backend is running:")
            print("  python run_backend.py")

if __name__ == "__main__":
    asyncio.run(test_branding_logos())
