from playwright.sync_api import sync_playwright

def save_twitter_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            viewport={"width": 1280, "height": 720},
            locale="en-US",
            timezone_id="Europe/Dublin"
        )
        page = context.new_page()

        page.goto("https://twitter.com/login")

        input("⚠️ After logging in manually, press Enter to continue...")

        # Save cookies and localStorage
        context.storage_state(path="data/twitter_cookies.json")
        print("✅ Login successfully saved in 'twitter_cookies.json'.")

        browser.close()

if __name__ == "__main__":
    save_twitter_login()