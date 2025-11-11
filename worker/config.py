"""
Configuration settings for the scraper worker.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings.
    
    These can be overridden by environment variables.
    """
    
    # Scraper settings
    headless: bool = True
    timeout: int = 30000  # milliseconds
    max_concurrent_scrapes: int = 5
    
    # Browser settings
    viewport_width: int = 1920
    viewport_height: int = 1080
    user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    
    # Retry settings
    max_retries: int = 3
    retry_delay: int = 2  # seconds
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
