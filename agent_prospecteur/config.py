import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # API Keys
    GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    
    # Email Settings
    SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "prospection@example.com")
    
    # App Settings
    ANTIGRAVITY_FLIGHT = os.getenv("ANTIGRAVITY_FLIGHT", "0") == "1"
    DB_PATH = os.getenv("DB_PATH", "prospects.db")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Limits
    MAX_PROSPECTS = 50 
    
    @classmethod
    def validate(cls):
        """Check if critical keys are present (unless in Flight Mode)."""
        if cls.ANTIGRAVITY_FLIGHT:
            return True
            
        missing = []
        if not cls.GOOGLE_PLACES_API_KEY: missing.append("GOOGLE_PLACES_API_KEY")
        if not cls.OPENAI_API_KEY: missing.append("OPENAI_API_KEY")
        # Hunter and SendGrid might be optional depending on flow, but let's warn
        if not cls.SENDGRID_API_KEY: missing.append("SENDGRID_API_KEY")
        
        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")
