from playwright.async_api import async_playwright
import json
import re 
from utils import rotate_user_agent, configure_stealth_browser, modify_browser_fingerprint, simulate_human_behavior
import random
import asyncio

async def simulate_human_scroll(page, times=5, delay=2):
    for _ in range(times):
        await page.mouse.wheel(0, 2500)
        await page.wait_for_timeout(delay * 1000)

async def search_twitter_and_scrape(term="python", newest = False, max_tweets=50):
    async with async_playwright() as p:
        # Tip 1: Browser configuration
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled", 
                  "--disable-infobars",
                  "--disable-blink-features"
                  ],
            )
        
        context = await browser.new_context(
            storage_state="data/twitter_cookies.json",
            locale="en-US",
            timezone_id="Europe/Dublin",
            permissions=["geolocation"]
        )

        # Tip 2: Browser fingerprint modification
        page = await context.new_page()
        page = await configure_stealth_browser(page)
        page = await modify_browser_fingerprint(page)

        try:
            # Tip 3: Randomize User Agent
            user_agent = rotate_user_agent()
            await page.set_extra_http_headers({"User-Agent": user_agent})
        
            await page.goto("https://twitter.com/login")
            await page.wait_for_timeout(random.uniform(2000, 3000))
            # Tip 4: Natural  Scrolling Behavior
            for i in range(3):
                await page.mouse.wheel(delta_y=random.randint(300, 500), delta_x=random.randint(300, 500))
                await asyncio.sleep(random.uniform(1, 2))

            # Tip 5: Random Delays and Human-like Behavior
            await simulate_human_behavior(page)
            await page.wait_for_timeout(random.uniform(2000, 3000))

            # Clicks on the search bar
            search_input = page.locator("input[aria-label='Search query']")
            await search_input.hover()
            await search_input.click()
            await page.keyboard.type(term, delay=150)
            await page.keyboard.press("Enter")

            await page.wait_for_timeout(5000)

            if newest:    
                filter_button = page.locator("span:has-text('Latest')")
                await filter_button.hover()
                await filter_button.click()
                await page.wait_for_timeout(3000)

            tweet_data = []
            seen_tweets = set()

            while len(tweet_data) < max_tweets:
                # Simulates human scrolling
                # await simulate_human_scroll(page, times=1, delay=2)

                # Captures tweets
                tweets = page.locator("article")
                print(f"🔎 {await tweets.count()} tweets found on the page.")

                for i in range(await tweets.count()):
                    tweet = tweets.nth(i)
                    await tweet.hover()
                    await page.wait_for_timeout(random.uniform(1000, 3000))

                    try:
                        
                        tweet_text_element = tweet.locator("div[lang]")
                        tweet_text = await tweet_text_element.inner_text()
                        
                        user_name_field = tweet.locator("div[data-testid='User-Name']").nth(0)
                        user_name = (await user_name_field.inner_text()).split("\n")[0]

                        user_handle_element = user_name_field.locator("a[role='link']").nth(0)
                        user_handle = await user_handle_element.get_attribute("href")
                        user_handle = user_handle.replace("/", "@")

                        timestamp_element = tweet.locator("time")
                        timestamp = await timestamp_element.get_attribute("datetime")

                        avatar_url_element = tweet.locator("div[data-testid='Tweet-User-Avatar'] img")
                        avatar_url = await avatar_url_element.get_attribute("src")

                        tweet_link_element = tweet.locator("time").locator("..")
                        tweet_link = await tweet_link_element.get_attribute("href")

                        # Captures tweet interactions (replies, reposts, likes, etc.)
                        interactions_element = tweet.locator("div[role='group']")
                        interactions = await interactions_element.get_attribute("aria-label")
                        replies, reposts, likes, saved_items = 0, 0, 0, 0  # Default values

                        if interactions:
                            # Uses regular expressions to extract numbers
                            replies_match = re.search(r"(\d+)\s+(reply|replies)", interactions)
                            reposts_match = re.search(r"(\d+)\s+(repost|reposts)", interactions)
                            likes_match = re.search(r"(\d+)\s+(like|likes)", interactions)
                            saved_items_match = re.search(r"(\d+)\s+(bookmark|bookmarks)", interactions)
                            view_match = re.search(r"(\d+)\s+(view|views)", interactions)

                            # Extracts corresponding values or keeps the default 0
                            replies = int(replies_match.group(1)) if replies_match else 0
                            reposts = int(reposts_match.group(1)) if reposts_match else 0
                            likes = int(likes_match.group(1)) if likes_match else 0
                            saved_items = int(saved_items_match.group(1)) if saved_items_match else 0
                            view = int(view_match.group(1)) if view_match else 0

                        # Creates a unique identifier for the tweet
                        tweet_id = f"{user_handle}-{timestamp}"

                        if tweet_id not in seen_tweets:
                            seen_tweets.add(tweet_id)
                            tweet_data.append({
                                "text": tweet_text,
                                "user_name": user_name,
                                "user_handle": user_handle,
                                "timestamp": timestamp,
                                "avatar_url": avatar_url,
                                "link": f"https://twitter.com{tweet_link}",
                                "replies": replies,
                                "reposts": reposts,
                                "likes": likes,
                                "saved_items": saved_items,
                                "view": view
                            })

                            print(f"\n--- TWEET {len(tweet_data)} ---")
                            print(json.dumps(tweet_data[-1], indent=4, ensure_ascii=False))

                            # Stops when the tweet limit is reached
                            if len(tweet_data) >= max_tweets:
                                break
                    except Exception as e:
                        print(f"Error capturing data for tweet {i+1}: {e}")

                # Checks if there are no new tweets
                if len(tweet_data) < max_tweets and await tweets.count() == 0:
                    print("No new tweets found. Finishing...")
                    break
            # Saves the data to a JSON file
            with open("data/raw/tweets.json", "w", encoding="utf-8") as f:
                json.dump(tweet_data, f, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"An error occurred: {e}")    

        

        await browser.close()

if __name__ == "__main__":
    asyncio.run(search_twitter_and_scrape("Barcelona", newest = False, max_tweets=20))