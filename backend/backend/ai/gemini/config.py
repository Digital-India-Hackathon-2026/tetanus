import os
import logging
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiConfig:
    """Configuration class for Gemini API settings."""
    
    API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DEFAULT_MODEL: str = os.getenv("GEMINI_DEFAULT_MODEL", "gemini-flash-lite-latest")
    DEFAULT_TEMPERATURE: float = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
    DEFAULT_MAX_TOKENS: int = int(os.getenv("GEMINI_MAX_TOKENS", "2048"))
    DEFAULT_TOP_P: float = float(os.getenv("GEMINI_TOP_P", "0.95"))
    DEFAULT_TOP_K: int = int(os.getenv("GEMINI_TOP_K", "40"))
    
    # Timeouts and limits
    TIMEOUT_SECONDS: int = int(os.getenv("GEMINI_TIMEOUT_SECONDS", "30"))
    MAX_RETRIES: int = int(os.getenv("GEMINI_MAX_RETRIES", "3"))
    MAX_CONCURRENT_REQUESTS: int = int(os.getenv("GEMINI_MAX_CONCURRENT_REQUESTS", "5"))

    @classmethod
    def validate(cls):
        """Validate critical configuration elements."""
        if not cls.API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is missing or empty.")
