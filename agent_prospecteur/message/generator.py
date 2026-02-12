import openai
from ..config import Config

class MessageGenerator:
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        if self.api_key:
            openai.api_key = self.api_key

    def generate(self, prospect):
        """
        Generate a personalized email for the prospect.
        Args:
            prospect (dict): Contains name, city, sector, valid_reasons (list), website_status
        Returns:
            str: Generated email content
        """
        if Config.ANTIGRAVITY_FLIGHT:
            return f"Subject: Proposal for {prospect['name']}\n\n[MOCK EMAIL CONTENT]\nWe noticed your site is archaic..."

        if not self.api_key:
            return "Error: OpenAI API Key missing."

        system_prompt = """
        You are an expert sales representative for a modern web agency. 
        Your goal is to write a short, professional, and warm cold-email (less than 150 words) to a business owner.
        You offer web design renovation or creation services.
        Avoid marketing jargon, be direct and helpful.
        End with a clear call to action (e.g., a free audit or a call).
        """
        
        user_prompt = f"""
        Prospect Name: {prospect['name']}
        City: {prospect['city']}
        Sector: {prospect['sector']}
        
        Situation:
        The prospect { 'has no website' if prospect['website_status'] == 'NO_SITE' else 'has an outdated website' }.
        
        Specific issues observed:
        {', '.join(prospect.get('valid_reasons', []))}
        
        Write the email content (Subject + Body).
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating message: {str(e)}"
