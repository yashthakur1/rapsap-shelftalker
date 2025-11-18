"""
Brand configuration for templates.
Defines available brands with logos, colors, and typography.
"""

BRAND_CONFIGS = {
    "frame27": {
        "id": "frame27",
        "name": "Frame 27",
        "logo_url": "/logos/Frame_27.png",
        "colors": {
            "primary": "#5074F3",
            "accent": "#2F448D",
            "text": "#000000",
            "textLight": "#FFFFFF",
            "background": "#FFFFFF",
            "backgroundGray": "#C5C8CD"
        },
        "fonts": {
            "heading": "'Barlow Condensed', Arial, sans-serif",
            "body": "'DM Sans', Arial, sans-serif"
        }
    },
    "logow": {
        "id": "logow",
        "name": "Logo W",
        "logo_url": "/logos/Logo_w.png",
        "colors": {
            "primary": "#5074F3",
            "accent": "#2F448D",
            "text": "#000000",
            "textLight": "#FFFFFF",
            "background": "#FFFFFF",
            "backgroundGray": "#C5C8CD"
        },
        "fonts": {
            "heading": "'Barlow Condensed', Arial, sans-serif",
            "body": "'DM Sans', Arial, sans-serif"
        }
    },
    "symbolb": {
        "id": "symbolb",
        "name": "Symbol Logo B",
        "logo_url": "/logos/Symbol_Logo_B.png",
        "colors": {
            "primary": "#5074F3",
            "accent": "#2F448D",
            "text": "#000000",
            "textLight": "#FFFFFF",
            "background": "#FFFFFF",
            "backgroundGray": "#C5C8CD"
        },
        "fonts": {
            "heading": "'Barlow Condensed', Arial, sans-serif",
            "body": "'DM Sans', Arial, sans-serif"
        }
    },
    "default": {
        "id": "default",
        "name": "Default (No Logo)",
        "logo_url": None,
        "colors": {
            "primary": "#0033cc",
            "accent": "#1a1aff",
            "text": "#030303",
            "textLight": "#FFFFFF",
            "background": "#FFFFFF",
            "backgroundGray": "#F5F5F5"
        },
        "fonts": {
            "heading": "'Arial', 'Helvetica', sans-serif",
            "body": "'Arial', 'Helvetica', sans-serif"
        }
    }
}

def get_brand_config(brand_name: str = "default") -> dict:
    """Get brand configuration by name"""
    return BRAND_CONFIGS.get(brand_name, BRAND_CONFIGS["default"])

def get_available_brands() -> list:
    """Get list of available brand names"""
    return list(BRAND_CONFIGS.keys())
