from bs4 import BeautifulSoup
import re

class DesignAnalyzer:
    def __init__(self):
        pass

    def analyze(self, html_content):
        """
        Analyze HTML content to determine if the design is archaic.
        Returns:
            status (str): 'ARCHAIC', 'MODERN', or 'UNKNOWN'
            reasons (list): List of reasons for the classification
        """
        if not html_content:
            return 'UNKNOWN', ["No content to analyze"]

        soup = BeautifulSoup(html_content, 'html.parser')
        reasons = []
        score = 0 # Higher means more archaic

        # 1. Check for Viewport Meta Tag (Mobile Responsiveness)
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if not viewport:
            score += 3
            reasons.append("Missing viewport meta tag (not responsive)")

        # 2. Check for old copyright year
        footer = soup.find('footer') or soup.find('div', class_='footer') or soup.find('div', id='footer')
        if footer:
            text = footer.get_text()
            years = re.findall(r'20\d{2}', text)
            if years:
                latest_year = max(int(y) for y in years)
                if latest_year < 2020:
                    score += 2
                    reasons.append(f"Copyright year is old: {latest_year}")
        
        # 3. Check for Tables used for layout (simple heuristic: many nested tables)
        tables = soup.find_all('table')
        if len(tables) > 5: # Arbitrary threshold for "too many tables"
            # Check if likely layout tables (no thread/tbody or specific classes)
            # This is a weak heuristic but okay for now
            score += 1
            reasons.append("Possible table-based layout detected")

        # 4. Check for Flash or Frames
        if soup.find('object') or soup.find('embed'):
            score += 5
            reasons.append("Flash content detected")
        
        if soup.find('frameset') or soup.find('frame'):
            score += 5
            reasons.append("Frameset detected")

        # 5. Check for Modern Frameworks (Bonus for Modern)
        html_str = html_content.lower()
        if 'bootstrap' in html_str or 'tailwind' in html_str or 'react' in html_str or 'vue' in html_str:
            score -= 5
            reasons.append("Modern framework detected")

        # Classification
        if score >= 3:
            return 'ARCHAIC', reasons
        elif score <= 0:
            return 'MODERN', reasons
        else:
            return 'UNKNOWN', reasons # Ambiguous, maybe simple site but not archaic
