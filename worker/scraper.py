"""
Web Scraper Worker Module

This module provides a scalable web scraping solution using Playwright.
It can be triggered multiple times and is designed for concurrent usage.
"""

from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from typing import Dict, Optional, Any
from datetime import datetime
import asyncio
from urllib.parse import urlparse


class WebScraper:
    """
    Scalable web scraper using Playwright.
    
    This class manages browser instances and provides a simple interface
    to scrape webpages and extract HTML content, URL, and metadata.
    """
    
    def __init__(self, headless: bool = True, timeout: int = 30000):
        """
        Initialize the scraper.
        
        Args:
            headless: Whether to run browser in headless mode
            timeout: Page load timeout in milliseconds (default: 30 seconds)
        """
        self.headless = headless
        self.timeout = timeout
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
    
    async def __aenter__(self):
        """Context manager entry - initialize browser."""
        await self._initialize_browser()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup browser."""
        await self.close()
        return False
    
    async def _initialize_browser(self):
        """Initialize the Playwright browser instance."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
    
    async def scrape(self, url: str, wait_for_selector: Optional[str] = None) -> Dict[str, Any]:
        """
        Scrape a single webpage and return HTML content, URL, and metadata.
        
        This is the main function to call for scraping. It handles:
        - Page navigation
        - Content extraction
        - Metadata collection
        - Error handling
        
        Args:
            url: The URL to scrape
            wait_for_selector: Optional CSS selector to wait for before scraping
        
        Returns:
            Dictionary containing:
                - url: The final URL (after any redirects)
                - html: The page HTML content
                - title: Page title
                - meta: Dictionary of metadata (description, keywords, etc.)
                - status_code: HTTP status code
                - timestamp: When the scrape was performed
                - success: Boolean indicating if scrape was successful
                - error: Error message if scrape failed
        """
        if not self.browser or not self.context:
            await self._initialize_browser()
        
        page: Optional[Page] = None
        result = {
            'url': url,
            'html': None,
            'title': None,
            'meta': {},
            'status_code': None,
            'timestamp': datetime.utcnow().isoformat(),
            'success': False,
            'error': None
        }
        
        try:
            # Create new page
            page = await self.context.new_page()
            page.set_default_timeout(self.timeout)
            
            # Navigate to URL
            response = await page.goto(url, wait_until='networkidle')
            
            if response:
                result['status_code'] = response.status
                result['url'] = page.url  # Get final URL after redirects
            
            # Wait for specific selector if provided
            if wait_for_selector:
                await page.wait_for_selector(wait_for_selector)
            
            # Extract page content
            result['html'] = await page.content()
            result['title'] = await page.title()
            
            # Extract metadata
            result['meta'] = await self._extract_metadata(page)
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
        
        finally:
            if page:
                try:
                    await page.close()
                except Exception:
                    pass  # Page already closed
        
        return result
    
    async def _extract_metadata(self, page: Page) -> Dict[str, Any]:
        """
        Extract metadata from the page.
        
        Args:
            page: Playwright Page object
        
        Returns:
            Dictionary containing meta tags and other metadata
        """
        metadata = {}
        
        try:
            # Extract common meta tags
            meta_tags = await page.query_selector_all('meta')
            
            for meta in meta_tags:
                name = await meta.get_attribute('name')
                property_attr = await meta.get_attribute('property')
                content = await meta.get_attribute('content')
                
                if name and content:
                    metadata[name] = content
                elif property_attr and content:
                    metadata[property_attr] = content
            
            # Extract canonical URL if exists
            canonical = await page.query_selector('link[rel="canonical"]')
            if canonical:
                metadata['canonical'] = await canonical.get_attribute('href')
            
            # Extract language
            html_element = await page.query_selector('html')
            if html_element:
                lang = await html_element.get_attribute('lang')
                if lang:
                    metadata['language'] = lang
        
        except Exception as e:
            metadata['extraction_error'] = str(e)
        
        return metadata
    
    async def close(self):
        """Close the browser and cleanup resources."""
        try:
            if self.context:
                await self.context.close()
        except Exception:
            pass  # Already closed
        
        try:
            if self.browser:
                await self.browser.close()
        except Exception:
            pass  # Already closed
        
        try:
            if hasattr(self, 'playwright'):
                await self.playwright.stop()
        except Exception:
            pass  # Already stopped


# Simple function interface for single scrapes
async def scrape_url(url: str, headless: bool = True, 
                     wait_for_selector: Optional[str] = None) -> Dict[str, Any]:
    """
    Simple function to scrape a URL. This is the main entry point.
    
    Use this function when you need to scrape a single URL without
    managing the browser lifecycle yourself.
    
    Args:
        url: The URL to scrape
        headless: Whether to run browser in headless mode
        wait_for_selector: Optional CSS selector to wait for
    
    Returns:
        Dictionary containing scraped data and metadata
    
    Example:
        result = await scrape_url('https://example.com')
        if result['success']:
            print(result['html'])
            print(result['title'])
            print(result['meta'])
    """
    async with WebScraper(headless=headless) as scraper:
        return await scraper.scrape(url, wait_for_selector)


def scrape_url_sync(url: str, headless: bool = True, 
                    wait_for_selector: Optional[str] = None) -> Dict[str, Any]:
    """
    Synchronous wrapper for scrape_url.
    
    Use this when you need to call the scraper from synchronous code.
    
    Args:
        url: The URL to scrape
        headless: Whether to run browser in headless mode
        wait_for_selector: Optional CSS selector to wait for
    
    Returns:
        Dictionary containing scraped data and metadata
    
    Example:
        result = scrape_url_sync('https://example.com')
        if result['success']:
            print(result['html'])
    """
    try:
        # Check if we're already in an event loop
        loop = asyncio.get_running_loop()
        # If we are, we can't use asyncio.run(), so we need a different approach
        import concurrent.futures
        import threading
        
        def run_in_thread():
            return asyncio.run(scrape_url(url, headless, wait_for_selector))
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_in_thread)
            return future.result()
    except RuntimeError:
        # No event loop running, safe to use asyncio.run()
        return asyncio.run(scrape_url(url, headless, wait_for_selector))


# For batch scraping multiple URLs efficiently
async def scrape_urls_batch(urls: list[str], headless: bool = True, 
                            max_concurrent: int = 5) -> list[Dict[str, Any]]:
    """
    Scrape multiple URLs concurrently with controlled concurrency.
    
    This function reuses the same browser instance for efficiency
    and limits concurrent scraping to avoid overwhelming resources.
    
    Args:
        urls: List of URLs to scrape
        headless: Whether to run browser in headless mode
        max_concurrent: Maximum number of concurrent scrapes
    
    Returns:
        List of dictionaries containing scraped data
    
    Example:
        urls = ['https://example.com', 'https://example.org']
        results = await scrape_urls_batch(urls)
        for result in results:
            print(f"{result['url']}: {result['success']}")
    """
    async with WebScraper(headless=headless) as scraper:
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def scrape_with_limit(url: str):
            async with semaphore:
                return await scraper.scrape(url)
        
        tasks = [scrape_with_limit(url) for url in urls]
        return await asyncio.gather(*tasks)
