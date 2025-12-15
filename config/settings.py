
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings and configuration"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    BRIA_API_KEY = os.getenv("BRIA_API_KEY")
    
    # Page Configuration
    PAGE_TITLE = "Context Chameleon | Bria FIBO Engine"
    PAGE_LAYOUT = "wide"
    
    # Image Generation
    DEFAULT_IMAGE_WIDTH = 1024
    DEFAULT_IMAGE_HEIGHT = 1024
    MAX_PRODUCT_SIZE_RATIO = 0.6
    
    # API Settings
    BRIA_API_ENDPOINT = "https://engine.prod.bria-api.com/v2/image/generate"
    GEMINI_MODEL = "gemini-flash-lite-latest"
    MAX_POLL_ATTEMPTS = 30
    POLL_INTERVAL = 2  # seconds
    
    @classmethod
    def has_api_keys(cls) -> bool:
        """Check if both API keys are configured"""
        return bool(cls.GEMINI_API_KEY and cls.BRIA_API_KEY)