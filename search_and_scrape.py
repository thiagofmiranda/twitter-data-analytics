from playwright.sync_api import sync_playwright
import json
import re 

def simulate_human_scroll(page, times=5, delay=2):
    for _ in range(times):
        page.mouse.wheel(0, 2500)
        page.wait_for_timeout(delay * 1000)

def search_twitter_and_scrape(term="python", max_tweets=50):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        context = browser.new_context(
            storage_state="data/twitter_cookies.json",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            viewport={"width": 1280, "height": 720},
            locale="en-US",
            timezone_id="Europe/Dublin"
        )

        page = context.new_page()

        page.goto("https://twitter.com/login")
        page.wait_for_timeout(3000)

        # Clicks on the search bar
        search_input = page.locator("input[aria-label='Search query']")
        search_input.click()
        page.keyboard.type(term, delay=150)
        page.keyboard.press("Enter")

        page.wait_for_timeout(5000)

        filter_button = page.locator("span:has-text('Latest')")
        filter_button.click()
        page.wait_for_timeout(3000)

        tweet_data = []
        seen_tweets = set()

        while len(tweet_data) < max_tweets:
            # Simulates human scrolling
            simulate_human_scroll(page, times=1, delay=2)

            # Captures tweets
            tweets = page.locator("article")
            print(f"🔎 {tweets.count()} tweets found on the page.")

            for i in range(tweets.count()):
                tweet = tweets.nth(i)
                try:
                    # Captures tweet information
                    tweet_text = tweet.locator("div[lang]").inner_text()
                    user_name_field = tweet.locator("div[data-testid='User-Name']").first
                    user_name = user_name_field.inner_text().split("\n")[0]
                    user_handle = user_name_field.locator("a[role='link']").first.get_attribute("href")
                    user_handle = user_handle.replace("/", "@")
                    timestamp = tweet.locator("time").get_attribute("datetime")
                    avatar_url = tweet.locator("div[data-testid='Tweet-User-Avatar'] img").get_attribute("src")
                    tweet_link = tweet.locator("time").locator("..").get_attribute("href")

                    # Captures tweet interactions (replies, reposts, likes, etc.)
                    interactions = tweet.locator("div[role='group']").get_attribute("aria-label")
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
            if len(tweet_data) < max_tweets and tweets.count() == 0:
                print("No new tweets found. Finishing...")
                break

        # Saves the data to a JSON file
        with open("data/raw/tweets.json", "w", encoding="utf-8") as f:
            json.dump(tweet_data, f, indent=4, ensure_ascii=False)

        browser.close()

if __name__ == "__main__":
    search_twitter_and_scrape("Barcelona", max_tweets=20)