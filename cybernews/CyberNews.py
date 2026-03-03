import json
import logging
from .extractor import Extractor

# C2SI Standard: Use logging for production-ready debugging
logger = logging.getLogger(__name__)

class CyberNews:
    def __init__(self) -> None:
        self._extractor = Extractor()
        # Ensure pathing is robust
        self._news_types = self.load_news_types_from_json('cybernews/news_types.json')

    def load_news_types_from_json(self, json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # Your JSON is a list of category-objects: [{"general": [...]}, {"malware": [...]}]
                return data if isinstance(data, list) else []
        except FileNotFoundError:
            logger.error(f"Critical Error: {json_file} not found.")
            return []

    def get_news_types(self) -> list:
        """Returns all category names available in the JSON config."""
        categories = []
        for item in self._news_types:
            categories.extend(item.keys())
        return categories

    def get_news(self, news_category) -> list:
        """
        Extracts news for a specific category. 
        Aligns the data format for the Extractor.
        """
        # 1. Extract the specific source list for the category
        # Since self._news_types is a list of dicts, we find the one matching the key
        category_data = next((item[news_category] for item in self._news_types if news_category in item), None)

        if not category_data:
            logger.warning(f"Category '{news_category}' not found in news_types.json.")
            return []

        try:
            # 2. Format it as a list that the Extractor expects
            # We wrap it in a dictionary to match the 'category_dict' loop in your data_extractor
            formatted_input = [{news_category: category_data}]
            
            # 3. Call Extractor (which handles threading and sorting)
            return self._extractor.data_extractor(formatted_input)
            
        except Exception as e:
            logger.error(f"Extraction failed for {news_category}: {str(e)}")
            return []