"""Simple test to debug scraper."""

import asyncio
from playwright.async_api import async_playwright

async def test_playwright_direct():
    """Test Playwright directly without our wrapper."""
    print("Testing Playwright directly...")
    
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()
    
    try:
        print("Navigating to example.com...")
        response = await page.goto('https://example.com', wait_until='load', timeout=30000)
        print(f"Response status: {response.status if response else 'None'}")
        
        title = await page.title()
        html = await page.content()
        
        print(f"Success! Title: {title}")
        print(f"HTML length: {len(html)}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        print("Closing resources...")
        try:
            await page.close()
        except:
            pass
        try:
            await browser.close()
        except:
            pass
        try:
            await p.stop()
        except:
            pass
        print("Done!")

if __name__ == "__main__":
    asyncio.run(test_playwright_direct())
