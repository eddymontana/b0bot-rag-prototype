"""
Class for Exception Handling and Extracting data out of complex strings
Optimized for C2SI b0bot Standard 2026
"""
import concurrent.futures
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from .performance import Performance
from .sorting import Sorting

class Extractor(Performance):
    def __init__(self):
        """
        Initializing the Extractor class with Parent Performance metrics.
        """
        super().__init__()
        # Use a connection pool for better performance in threads
        self.session = httpx.Client(http2=True, verify=False)
        self.sorting = Sorting()
        self.headers = self.headers()  # Inherited from Performance

    def _get_attribute_safely(self, element, selector_type, base_url=None):
        """
        Internal utility to bypass lazy loading and handle relative URLs.
        """
        if not element:
            return "N/A"

        if selector_type == "image":
            # Check multiple lazy-loading attributes common in news sites
            attributes = ['data-src', 'data-lazy-src', 'srcset', 'src', 'data-original']
            for attr in attributes:
                val = element.get(attr)
                if val:
                    # Handle srcset (take first image)
                    if attr == 'srcset':
                        val = val.split(',')[0].split(' ')[0]
                    return urljoin(base_url, val.strip()) if base_url else val.strip()

        elif selector_type == "link":
            val = element.get('href')
            if val:
                return urljoin(base_url, val.strip()) if base_url else val.strip()

        return "N/A"

    def _author_name_extractor(self, name: str):
        """Extracts and formats author name using regex patterns from Performance."""
        author_name = self.remove_symbols(self._pattern1.sub("", name))
        if not self.is_valid_author_name(author_name):
            return "N/A"
        return self.format_author_name(author_name)

    def _check_ad(self, news_date: str):
        """Checks if the date string is actually an ad indicator."""
        return self._pattern4.search(news_date) is not None

    def _news_date_extractor(self, date_str: str) -> str:
        """Extracts news date using patterns from Performance class."""
        # Clean the date string using inherited patterns
        clean_date = self._pattern3.sub("", self._pattern2.sub("", date_str))
        match = self._pattern5.match(clean_date)
        return match.group() if match else "N/A"

    def _extract_data_from_single_news(self, url: str, value: dict):
        """
        Extract data from a single news article source based on JSON selectors.
        """
        news_data_from_single_news = []
        try:
            response = self.session.get(url, timeout=20, headers=self.headers)
            soup = BeautifulSoup(response.text, "lxml")
        except Exception as e:
            print(f"Request to {url} failed: {e}")
            return []

        # Map JSON keys to Soup selectors
        headlines = soup.select(value.get("headlines", ""))
        authors = soup.select(value["author"]) if value.get("author") else []
        full_news = soup.select(value.get("fullNews", ""))
        urls = soup.select(value.get("newsURL", ""))
        images = soup.select(value.get("newsImg", ""))
        dates = soup.select(value["date"]) if value.get("date") else []

        for index in range(len(headlines)):
            try:
                # 1. Date Extraction
                raw_date = dates[index].text.strip() if index < len(dates) else ""
                news_date = self._news_date_extractor(raw_date) if raw_date else "N/A"
                
                if self._check_ad(news_date):
                    continue

                # 2. Author Extraction
                raw_author = authors[index].text.strip() if index < len(authors) else ""
                news_author = self._author_name_extractor(raw_author) if raw_author else "N/A"

                # 3. URL Extraction via Utility (Handles relative links)
                link_tag = urls[index] if index < len(urls) else None
                target_url = self._get_attribute_safely(link_tag, "link", base_url=url)
                
                if target_url == "N/A" or not self.valid_url_check(target_url):
                    continue

                # 4. Content & Spam Check
                headline_text = headlines[index].text.strip()
                body_text = full_news[index].text.strip() if index < len(full_news) else ""
                
                if self.spam_content_check(headline_text + " " + body_text):
                    continue

                # 5. Image Extraction via Utility (Bypasses lazy loading)
                img_tag = images[index] if index < len(images) else None
                img_url = self._get_attribute_safely(img_tag, "image", base_url=url)

                # ALIGNMENT: Use sort_key for date-logic and id for the final hash (in Sorting)
                complete_news = {
                    "sort_key": self.sorting.ordering_date(news_date),
                    "headlines": headline_text,
                    "author": news_author,
                    "fullNews": body_text,
                    "newsURL": target_url,
                    "newsImgURL": img_url,
                    "newsDate": news_date,
                    "source": url
                }
                news_data_from_single_news.append(complete_news)
            except Exception:
                continue

        return self._remove_duplicates(news_data_from_single_news)

    def data_extractor(self, news_config_list: list) -> list:
        """
        Threading Engine: Processes multiple news categories/URLs in parallel.
        """
        news_data = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {}
            for category_dict in news_config_list:
                for category, sources in category_dict.items():
                    for source in sources:
                        # source is a dict like {"https://url...": {selectors...}}
                        for url, selectors in source.items():
                            future = executor.submit(self._extract_data_from_single_news, url, selectors)
                            future_to_url[future] = url

            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                    news_data.extend(data)
                except Exception as exc:
                    print(f"{url} generated an exception: {exc}")

        # Final step: Sort by date and assign deterministic IDs (Hashes)
        return self.sorting.ordering_news(news_data)

    def _remove_duplicates(self, news_data: list) -> list:
        """Removes duplicates within a single source scrape."""
        seen = set()
        unique_data = []
        for item in news_data:
            identifier = (item["headlines"].lower(), item["newsURL"])
            if identifier not in seen:
                seen.add(identifier)
                unique_data.append(item)
        return unique_data