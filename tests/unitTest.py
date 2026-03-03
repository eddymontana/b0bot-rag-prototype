import unittest
import json
import os
import sys
from unittest.mock import patch
from dotenv import load_dotenv

# 1. Standard C2SI Path Logic
# Ensures the test can find 'app.py' and 'cybernews/' folder
current_file_path = os.path.abspath(__file__)
src_directory = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(src_directory)

# 2. Environment Setup
load_dotenv(os.path.join(src_directory, '.env'))
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        
    def tearDown(self):
        pass

    # --- THE MOCK TEST ---
    
    # Path Logic: cybernews (folder) . CyberNews (file) . CyberNews (class) . get_news (method)
    @patch('cybernews.CyberNews.CyberNews.get_news') 
    def test_news_with_mock(self, mock_get_news):
        """Verify the /news endpoint using a deterministic mock response."""
        
        # Define the 'Fake' data that matches your CyberNews format
        mock_get_news.return_value = [
            {
                "id": "test-id-001",
                "headlines": "C2SI Mock Intelligence Report",
                "newsURL": "https://c2si.example.com",
                "newsDate": "2026-03-03"
            }
        ]

        # Call the actual Flask route
        response = self.app.get('/news')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['headlines'], "C2SI Mock Intelligence Report")
        print("✅ SUCCESS: Flask route handled the Mocked CyberNews data correctly.")

    def test_invalid_route(self):
        """Standard 404 check."""
        response = self.app.get('/nonexistent_path')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()