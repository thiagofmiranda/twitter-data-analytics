import asyncio
import random
from fake_useragent import UserAgent
from playwright.async_api import async_playwright

async def modify_browser_fingerprint(page):
    await page.context.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    });
    // modify plataform
    Object.defineProperty(navigator, 'platform', {
        get: () => 'Win32'
    });
    // Override hardware concurrency
    Object.defineProperty(navigator, 'hardwareConcurrency', {
        get: () => 8
    });
    // Override memory info
    Object.defineProperty(navigator, 'deviceMemory', {
        get: () => 8
    });
    """)
    return page

def rotate_user_agent():
    ua = UserAgent()
    return ua.random

async def simulate_human_behavior(page):
    for _ in range(random.randint(3, 7)):
        # Random mouse movement
        await page.mouse.move(
            random.randint(100, 800), 
            random.randint(100, 600)
            )
    
    if random.random() < 0.7:
        await page.keyboard.press("Tab")
        await asyncio.sleep(random.uniform(0.1, 0.2))
    
    return page

async def configure_stealth_browser(page):
    await page.set_viewport_size({"width": 1280, "height": 800})

    # add extra headers
    await page.set_extra_http_headers({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Language": "gzip, deflate, br",
    })
    return page