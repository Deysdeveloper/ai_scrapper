"""
Web Scraper Worker Package

Provides scalable web scraping functionality using Playwright.
"""

from .scraper import scrape_url, scrape_url_sync, scrape_urls_batch, WebScraper
from .config import settings

__all__ = [
    'scrape_url',
    'scrape_url_sync', 
    'scrape_urls_batch',
    'WebScraper',
    'settings'
]

__version__ = '1.0.0'
