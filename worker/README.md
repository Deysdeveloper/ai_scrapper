# Web Scraper Worker

A scalable, production-ready web scraping worker built with Python and Playwright.

## Features

- ✅ **Simple Function Interface**: Call `scrape_url()` to scrape any webpage
- ✅ **Async & Sync Support**: Use async or synchronous versions
- ✅ **Batch Scraping**: Scrape multiple URLs concurrently with controlled concurrency
- ✅ **Rich Metadata**: Returns HTML, URL, title, meta tags, and more
- ✅ **Error Handling**: Comprehensive error handling with detailed error messages
- ✅ **Configurable**: Environment-based configuration
- ✅ **Docker Ready**: Containerized with all dependencies

## Installation

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install chromium
```

3. (Optional) Copy and configure environment variables:
```bash
cp .env.example .env
```

### Docker

Build the Docker image:
```bash
docker build -t scraper-worker .
```

## Usage

### Single URL Scraping (Async)

```python
import asyncio
from scraper import scrape_url

async def main():
    result = await scrape_url('https://example.com')
    
    if result['success']:
        print(f"Title: {result['title']}")
        print(f"HTML Length: {len(result['html'])}")
        print(f"Metadata: {result['meta']}")
    else:
        print(f"Error: {result['error']}")

asyncio.run(main())
```

### Single URL Scraping (Sync)

```python
from scraper import scrape_url_sync

result = scrape_url_sync('https://example.com')

if result['success']:
    print(f"Title: {result['title']}")
    print(f"Status: {result['status_code']}")
```

### Batch Scraping

```python
import asyncio
from scraper import scrape_urls_batch

async def main():
    urls = [
        'https://example.com',
        'https://example.org',
        'https://example.net'
    ]
    
    results = await scrape_urls_batch(urls, max_concurrent=3)
    
    for result in results:
        print(f"{result['url']}: {result['success']}")

asyncio.run(main())
```

### Advanced Usage with Context Manager

```python
import asyncio
from scraper import WebScraper

async def main():
    # Reuse browser instance for multiple scrapes
    async with WebScraper(headless=True) as scraper:
        result1 = await scraper.scrape('https://example.com')
        result2 = await scraper.scrape('https://example.org')
        result3 = await scraper.scrape('https://example.net')

asyncio.run(main())
```

### Wait for Specific Elements

```python
from scraper import scrape_url_sync

# Wait for a specific selector before scraping
result = scrape_url_sync(
    'https://example.com',
    wait_for_selector='#main-content'
)
```

## Response Structure

Each scrape returns a dictionary with the following structure:

```python
{
    'url': 'https://example.com',           # Final URL (after redirects)
    'html': '<html>...</html>',             # Full page HTML
    'title': 'Example Domain',              # Page title
    'meta': {                                # Metadata dictionary
        'description': 'Example site',
        'keywords': 'example, demo',
        'og:title': 'Example',
        'language': 'en',
        'canonical': 'https://example.com'
    },
    'status_code': 200,                      # HTTP status code
    'timestamp': '2024-01-15T10:30:00',     # When scrape was performed
    'success': True,                         # Whether scrape succeeded
    'error': None                            # Error message if failed
}
```

## Testing

Run the test suite:

```bash
python test_scraper.py
```

This will:
1. Test single URL scraping (async)
2. Test single URL scraping (sync)
3. Test batch scraping
4. Test scraping with wait selector
5. Save a sample result to `scrape_result.json`

## Configuration

Configure via environment variables or `.env` file:

```env
HEADLESS=true
TIMEOUT=30000
MAX_CONCURRENT_SCRAPES=5
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080
MAX_RETRIES=3
RETRY_DELAY=2
```

## Docker Usage

Run the worker in Docker:

```bash
docker run -e HEADLESS=true scraper-worker
```

With custom configuration:

```bash
docker run \
  -e HEADLESS=true \
  -e TIMEOUT=60000 \
  -e MAX_CONCURRENT_SCRAPES=10 \
  scraper-worker
```

## Architecture

The worker is designed to be:

- **Scalable**: Can handle multiple concurrent scrapes efficiently
- **Reusable**: Browser instances can be reused for multiple scrapes
- **Isolated**: Each scrape uses a new page context for isolation
- **Reliable**: Proper cleanup and error handling
- **Flexible**: Supports both async and sync interfaces

## Performance Considerations

- Browser instances are reused when using the `WebScraper` class directly
- Each scrape creates a new page context for isolation
- Concurrent scraping is controlled with semaphores to prevent resource exhaustion
- Default timeout is 30 seconds per page

## Error Handling

All errors are caught and returned in the result dictionary:

```python
result = scrape_url_sync('https://invalid-url.com')
if not result['success']:
    print(f"Scraping failed: {result['error']}")
```

## License

[Add your license here]
