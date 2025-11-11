"""
Test script for the web scraper.

Run this to verify the scraper works correctly.
"""

import asyncio
import json
from scraper import scrape_url, scrape_url_sync, scrape_urls_batch


async def test_single_scrape():
    """Test scraping a single URL asynchronously."""
    print("\n=== Testing Single URL Scrape (Async) ===")
    
    url = "https://example.com"
    result = await scrape_url(url)
    
    print(f"URL: {result['url']}")
    print(f"Success: {result['success']}")
    print(f"Status Code: {result['status_code']}")
    print(f"Title: {result['title']}")
    print(f"Timestamp: {result['timestamp']}")
    print(f"HTML Length: {len(result['html']) if result['html'] else 0} characters")
    print(f"Metadata Keys: {list(result['meta'].keys())}")
    
    if result['error']:
        print(f"Error: {result['error']}")
    
    return result


def test_single_scrape_sync():
    """Test scraping a single URL synchronously."""
    print("\n=== Testing Single URL Scrape (Sync) ===")
    
    url = "https://example.com"
    result = scrape_url_sync(url)
    
    print(f"URL: {result['url']}")
    print(f"Success: {result['success']}")
    print(f"Title: {result['title']}")
    print(f"Status Code: {result['status_code']}")
    
    return result


async def test_batch_scrape():
    """Test scraping multiple URLs in batch."""
    print("\n=== Testing Batch URL Scrape ===")
    
    urls = [
        "https://example.com",
        "https://example.org",
        "https://www.iana.org/domains/reserved"
    ]
    
    results = await scrape_urls_batch(urls, max_concurrent=2)
    
    print(f"Scraped {len(results)} URLs")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['url']}")
        print(f"   Success: {result['success']}")
        print(f"   Title: {result['title']}")
        if result['error']:
            print(f"   Error: {result['error']}")
    
    return results


async def test_with_wait_selector():
    """Test scraping with wait for selector."""
    print("\n=== Testing Scrape with Wait Selector ===")
    
    url = "https://example.com"
    # Wait for the main heading
    result = await scrape_url(url, wait_for_selector="h1")
    
    print(f"URL: {result['url']}")
    print(f"Success: {result['success']}")
    print(f"Title: {result['title']}")
    
    return result


def save_result_to_file(result, filename="scrape_result.json"):
    """Save scrape result to a JSON file."""
    # Remove HTML content for cleaner output
    result_copy = result.copy()
    if result_copy.get('html'):
        result_copy['html'] = f"<HTML content - {len(result_copy['html'])} characters>"
    
    with open(filename, 'w') as f:
        json.dump(result_copy, f, indent=2)
    
    print(f"\nResult saved to {filename}")


async def main():
    """Run all tests."""
    print("=" * 60)
    print("Web Scraper Test Suite")
    print("=" * 60)
    
    try:
        # Test 1: Single async scrape
        result1 = await test_single_scrape()
        
        # Test 2: Batch scrape
        result3 = await test_batch_scrape()
        
        # Test 3: Scrape with wait selector
        result4 = await test_with_wait_selector()
        
        # Save one result as example
        if result1['success']:
            save_result_to_file(result1)
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


def main_sync():
    """Test sync scraping separately."""
    print("\n" + "=" * 60)
    print("Testing Sync Scraper")
    print("=" * 60)
    test_single_scrape_sync()


if __name__ == "__main__":
    asyncio.run(main())
