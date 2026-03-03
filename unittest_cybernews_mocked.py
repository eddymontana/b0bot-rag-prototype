import unittest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.append(os.getcwd())
from cybernews.CyberNews import CyberNews

class TestCyberNewsMocked(unittest.TestCase):
    def setUp(self):
        # 1. Patch the Extractor
        self.extractor_patcher = patch('cybernews.CyberNews.Extractor')
        self.mock_extractor_class = self.extractor_patcher.start()
        self.mock_extractor_instance = self.mock_extractor_class.return_value
        
        # 2. Patch the JSON loader so we don't need a real news_types.json
        with patch.object(CyberNews, 'load_news_types_from_json') as mock_load:
            # We tell the class that 'general' exists in its config
            mock_load.return_value = [{"general": [{"url": "http://test.com"}]}]
            self.news_service = CyberNews()

    def tearDown(self):
        self.extractor_patcher.stop()

    def test_get_news_data_flow(self):
        """Verify that CyberNews correctly passes data to the Extractor."""
        fake_extracted_data = [
            {"headlines": "Mocked Intelligence", "newsURL": "http://test.com", "id": "hash-123"}
        ]
        self.mock_extractor_instance.data_extractor.return_value = fake_extracted_data

        # Now 'general' will be found because we mocked the config load!
        result = self.news_service.get_news("general")

        self.assertEqual(result, fake_extracted_data)
        self.mock_extractor_instance.data_extractor.assert_called_once()
        print("\n✅ Success: CyberNews -> Extractor flow verified (Mocked).")

    def test_invalid_category_logic(self):
        """Ensure invalid types are caught before the scraper is even triggered."""
        result = self.news_service.get_news("non_existent_category")
        self.assertEqual(result, [])
        self.mock_extractor_instance.data_extractor.assert_not_called()
        print("✅ Success: Invalid category logic verified.")

if __name__ == "__main__":
    unittest.main()