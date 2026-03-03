import re
from urllib.parse import urljoin

def get_attribute_safely(element, selector_type, base_url=None):
    """
    Checks multiple attributes to bypass lazy loading and handles 
    complex attributes like srcset.
    """
    # 1. Logic for Images
    if selector_type == "image":
        attributes = ['data-src', 'data-lazy-src', 'srcset', 'src', 'data-original']
        for attr in attributes:
            val = element.get(attr)
            if val:
                # If it's a srcset, grab the first URL before the space
                if attr == 'srcset':
                    val = val.split(',')[0].split(' ')[0]
                
                # Ensure the URL is absolute
                if base_url:
                    return urljoin(base_url, val.strip())
                return val.strip()

    # 2. Logic for Links
    elif selector_type == "link":
        val = element.get('href')
        if val and base_url:
            return urljoin(base_url, val.strip())
        return val

    return None