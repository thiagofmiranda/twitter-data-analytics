# Twitter Data Analytics

This project is a Python-based tool for scraping and analyzing tweets using Playwright. It allows you to log in to Twitter, search for specific terms, and scrape tweets with detailed metadata.

## Features

- **Login and Save Cookies**: Automates the login process and saves session cookies for reuse.
- **Search and Scrape Tweets**: Searches Twitter for a specific term and scrapes tweets, including metadata such as text, user details, timestamps, and interactions.
- **Simulated Human Scrolling**: Mimics human-like scrolling to load more tweets.
- **JSON Output**: Saves scraped tweets in a structured JSON format.

## Project Structure

```
.
├── .gitignore                # Specifies files to ignore in version control
├── login_and_save.py         # Script to log in to Twitter and save cookies
├── search_and_scrape.py      # Script to search and scrape tweets
├── data/
│   ├── twitter_cookies.json  # Saved Twitter cookies
│   └── raw/
│       └── tweets.json       # Scraped tweets data
```

## Requirements

- Python 3.7+
- Playwright
- Node.js (required for Playwright installation)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/twitter-data-analytics.git
   cd twitter-data-analytics
   ```

2. Install dependencies:
   ```bash
   pip install playwright
   playwright install
   ```

3. Install additional Python packages:
   ```bash
   pip install re json
   ```

## Usage

### 1. Save Twitter Login Session

Run the `login_and_save.py` script to log in to Twitter and save the session cookies:

```bash
python login_and_save.py
```

Follow the instructions to log in manually. Once logged in, the session cookies will be saved in `data/twitter_cookies.json`.

### 2. Search and Scrape Tweets

Run the `search_and_scrape.py` script to search for tweets and scrape data:

```bash
python search_and_scrape.py
```

You can customize the search term and the maximum number of tweets by modifying the `search_twitter_and_scrape` function call at the bottom of the script:

```python
search_twitter_and_scrape("YourSearchTerm", max_tweets=100)
```

### 3. View Scraped Data

The scraped tweets will be saved in `data/raw/tweets.json`. Open the file to view the data in JSON format.

## Notes

- Ensure that your Twitter account is active and not restricted to avoid issues during login or scraping.
- The `.gitignore` file is configured to exclude sensitive files like `twitter_cookies.json` from version control.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Disclaimer

This project is for educational purposes only. Scraping data from websites may violate their terms of service. Use this tool responsibly and ensure compliance with Twitter's policies.
