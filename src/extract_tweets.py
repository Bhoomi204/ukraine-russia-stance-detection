import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import time

def scrape_window(query, start, end, max_tweets=150):
    # Note product:Top helps when Latest is blocked
    q = f'{query} since:{start:%Y-%m-%d} until:{end:%Y-%m-%d} lang:en -filter:replies'
    items = sntwitter.TwitterSearchScraper(q, searchMode=sntwitter.TwitterSearchScraperMode.TOP).get_items()
    rows = []
    for i, t in enumerate(items):
        if i >= max_tweets: break
        rows.append([t.date, t.user.username, t.content, t.likeCount, t.retweetCount, t.replyCount, t.lang])
    return pd.DataFrame(rows, columns=['date','username','text','likes','retweets','replies','lang'])

def main():
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    keywords = ['"Ukraine Russia" OR "#StandWithUkraine"', '"Ukraine Russia" OR "#ISupportRussia"']
    start = datetime(2024,10,1)
    end   = datetime(2024,11,1)

    all_parts = []
    day = start
    while day < end:
        day_end = day + timedelta(days=1)
        for q in keywords:
            for attempt in range(2):  # one retry
                try:
                    print(f"Scraping: {q}  {day:%Y-%m-%d} → {day_end:%Y-%m-%d}")
                    df = scrape_window(q, day, day_end, max_tweets=120)
                    all_parts.append(df)
                    break
                except Exception as e:
                    print(f"  Warn: {e}  (retrying once in 8s)")
                    time.sleep(8)
        day = day_end

    out = pd.concat(all_parts, ignore_index=True) if all_parts else pd.DataFrame(columns=['date','username','text','likes','retweets','replies','lang'])
    out.drop_duplicates(subset='text', inplace=True)
    out.to_csv("data/raw/extracted_tweets.csv", index=False)
    print(f"✅ Saved {len(out)} unique tweets → data/raw/extracted_tweets.csv")

if __name__ == "__main__":
    main()