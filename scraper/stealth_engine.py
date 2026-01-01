import asyncio import random from playwright.async_api import async_playwright from playwright_stealth import stealth_async

Configuration for residential proxies

PROXIES = [ "http://user:pass@geo.proxy-provider.com:8000", "http://user:pass@geo.proxy-provider.com:8001" ]

async def scrape_car_data(url): async with async_playwright() as p: # Use a random residential proxy for this session proxy_server = random.choice(PROXIES)

    browser = await p.chromium.launch(
        headless=True,
        proxy={"server": proxy_server}
    )
    
    # Mimic a real user context
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={'width': 1920, 'height': 1080}
    )
    
    page = await context.new_page()
    
    # Apply stealth patches to evade bot detection
    await stealth_async(page)
    
    try:
        # Human-like delay jitter
        await asyncio.sleep(random.uniform(2, 5))
        
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="networkidle", timeout=60000)
        
        # Extract Car Details
        cars = await page.evaluate('''() => {
            const items = Array.from(document.querySelectorAll('.listing-card'));
            return items.map(item => ({
                make: item.querySelector('.make').innerText,
                model: item.querySelector('.model').innerText,
                price: item.querySelector('.price').innerText,
                year: item.querySelector('.year').innerText
            }));
        }''')
        
        return cars

    except Exception as e:
        print(f"Blocked or Timeout: {e}")
        return None
    finally:
        await browser.close()


if name == "main": url = "https://example-autos.com/search" results = asyncio.run(scrape_car_data(url)) print(results)