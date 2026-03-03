"""
Class for Sorting and Deduplication
Aligned with C2SI b0bot GSoC 2024-2026 Standards
"""
import uuid
import hashlib

class Sorting:
    def __init__(self) -> None:
        # ALIGNMENT: Added common abbreviations used in cyber news feeds
        self._months = {
            "january": "01", "february": "02", "march": "03", "april": "04",
            "may": "05", "june": "06", "july": "07", "august": "08",
            "september": "09", "october": "10", "november": "11", "december": "12",
            "jan": "01", "feb": "02", "mar": "03", "apr": "04", "jun": "06",
            "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"
        }

    def _generate_deterministic_id(self, url: str) -> str:
        """
        C2SI STANDARD: Generates a unique ID based on the URL.
        This prevents duplicate news entries in the Vector DB.
        """
        if not url:
            return str(uuid.uuid4())
        # Create a SHA-256 hash of the URL to ensure the same ID for the same article
        return hashlib.sha256(url.encode()).hexdigest()[:24]

    def ordering_date(self, date_string: str) -> int:
        """
        Converts date string to YYYYMMDD integer for chronological sorting.
        """
        if not date_string or date_string == "N/A":
            return 0

        # Standard C2SI cleaning: Lowercase and strip punctuation
        date_string = date_string.lower().replace(",", "").replace(".", "")
        parts = [p for p in date_string.split(" ") if p]

        try:
            # Handle DD Month YYYY or Month DD YYYY
            if parts[0].isdigit():
                day = parts[0].zfill(2)
                month = self._months.get(parts[1], "01")
                year = parts[2]
            else:
                month = self._months.get(parts[0], "01")
                day = parts[1].zfill(2)
                year = parts[2]
            
            return int(f"{year}{month}{day}")
        except (IndexError, KeyError):
            return 0

    def ordering_news(self, news_list: list) -> list:
        """
        1. Generates deterministic IDs based on source URLs.
        2. Sorts by the date-integer (latest first).
        """
        for item in news_list:
            # Assign deterministic ID instead of random UUID
            item["id"] = self._generate_deterministic_id(item.get("newsURL", ""))
            
            # Ensure a sort_key exists (generated via ordering_date in Extractor)
            # If not present, we generate it now
            if "sort_key" not in item:
                item["sort_key"] = self.ordering_date(item.get("date", "N/A"))

        # Sort by sort_key (Date) descending
        sorted_news = sorted(news_list, key=lambda x: x["sort_key"], reverse=True)
        
        return sorted_news