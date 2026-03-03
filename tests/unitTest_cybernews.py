"""
Unittest class for CyberNews
Aligned with C2SI 2026 Standards for B0Bot
"""
import unittest
from cybernews.CyberNews import CyberNews

class TestCyberNews(unittest.TestCase):
    def setUp(self):
        """Standard Setup: Initialize the scraper instance."""
        self.news = CyberNews()
        # ALIGNMENT: get_news_types() is a method, not a variable. 
        # We call it here to get the list for iteration.
        self.valid_categories = self.news.get_news_types()
        self.invalid_categories = ["", "Invalid_Category_999", None]

    def test_init(self):
        """Verify the scraper initializes and loads categories from JSON."""
        categories = self.news.get_news_types()
        self.assertIsInstance(categories, list)
        self.assertGreater(len(categories), 0, "JSON config failed to load categories.")

    def test_get_news_valid_types(self):
        """Integration Test: Ensure valid categories return a list (not necessarily full)."""
        # C2SI prefers explicit loops in tests for better failure reporting
        for category in self.valid_categories:
            with self.subTest(category=category):
                result = self.news.get_news(category)
                self.assertIsInstance(result, list, f"Category {category} did not return a list.")
                # Note: We don't assert len > 0 because a site might be temporarily down

    def test_get_news_invalid_type(self):
        """Error Handling: Ensure invalid types return an empty list gracefully."""
        # Based on your CyberNews.py, we return [] rather than raising ValueError
        # This aligns with the 'Non-Crashing API' standard for GSoC.
        for category in self.invalid_categories:
            with self.subTest(category=category):
                result = self.news.get_news(category)
                self.assertEqual(result, [], f"Invalid category {category} should return an empty list.")

if __name__ == "__main__":
    unittest.main()