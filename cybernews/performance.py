import re
from datetime import datetime

class Performance:
    # ALIGNMENT: Broaden range to catch all icon-font artifacts across different sites
    _pattern_unicode = re.compile(r"[\ue800-\ue8ff]") 
    _pattern_whitespace = re.compile(r"\s+")
    
    # ALIGNMENT: More robust URL check for Pinecone metadata validation
    _pattern_url = re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+")
    symbol_regex = re.compile(r"[^\w\s-]")

    def __init__(self):
        # ALIGNMENT: Removed 'server', 'etag', and 'x-runtime'. 
        # These were Response headers. Sending them in a Request is a bot-leak.
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        self._spam_keywords = ["buy now", "click here", "subscribe", "limited offer", "advertisement"]

    def remove_symbols(self, text: str) -> str:
        if not text: return ""
        # Clean unicode icons first, then format
        text = self._pattern_unicode.sub("", text)
        return re.sub(self.symbol_regex, "", text).strip()

    def check_valid_date(self, date_str: str) -> bool:
        # ALIGNMENT: Added common news formats to prevent 'N/A' on non-ET sites
        for fmt in ["%b %d %Y", "%d %b %Y", "%Y-%m-%d", "%B %d, %Y"]:
            try:
                datetime.strptime(date_str, fmt)
                return True
            except ValueError:
                continue
        return False

    # ... rest of your formatting logic ...
    

