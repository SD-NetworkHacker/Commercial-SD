import requests
import re
from urllib.parse import urlparse

class SiteChecker:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def check(self, url):
        """
        Check if a website is reachable.
        Returns: (is_reachable, final_url, html_content)
        """
        if not url:
            return False, None, None

        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        try:
            response = requests.get(url, headers=self.headers, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                return True, response.url, response.text
            return False, None, None
        except requests.RequestException:
            return False, None, None

    def guess_domain(self, business_name):
        """
        Guess a domain from business name and check if it exists.
        Returns: valid_url or None
        """
        # Clean name: remove special chars, spaces to dashes
        clean_name = re.sub(r'[^\w\s-]', '', business_name).strip().lower()
        slug = re.sub(r'[-\s]+', '-', clean_name)
        
        candidates = [
            f"www.{slug}.fr",
            f"www.{slug}.com",
            f"{slug}.fr",
            f"{slug}.com"
        ]

        for domain in candidates:
            is_up, url, _ = self.check(domain)
            if is_up:
                return url
        
        return None
