import requests
from ..config import Config

class EmailFinder:
    def __init__(self):
        self.api_key = Config.HUNTER_API_KEY
        self.base_url = "https://api.hunter.io/v2/domain-search"

    def find(self, domain, company_name=None):
        """
        Find email addresses for a domain or company name.
        Returns: email (str) or None
        """
        if Config.ANTIGRAVITY_FLIGHT:
            return f"contact@{domain or 'example.com'}"

        if not domain:
            return None

        email = self._find_with_hunter(domain)
        if email:
            return email
            
        # Fallback to common patterns if Hunter fails or no key
        return None # Return None to indicate failure to find *verified* email

    def _find_with_hunter(self, domain):
        if not self.api_key:
            return None
            
        params = {
            'domain': domain,
            'api_key': self.api_key,
            'limit': 1
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            emails = data.get('data', {}).get('emails', [])
            if emails:
                return emails[0].get('value')
        except Exception as e:
            print(f"Error calling Hunter API: {e}")
            
        return None
