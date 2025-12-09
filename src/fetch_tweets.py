import tweepy
import pandas as pd
import os

BEARER = os.getenv("TWITTER_BEARER_TOKEN")  # or hardcode (not recommended)
client = tweepy.Client(bearer_token=BEARER)

query = '("Ukraine Russia") OR "#StandWithUkraine" OR "#ISupportRussia" lang:en -is:retweet'

tweets = client.search_recent_tweets(query=query,
                max_results=400, tweet_fields=['created_at','lang','public_metrics'])

rows = []
for t in tweets.data or []:
    rows.append({
       "id": t.id,
       "date": t.created_at,
       "text": t.text,
       "like": t.public_metrics["like_count"],
       "retweet": t.public_metrics["retweet_count"],
    })

df = pd.DataFrame(rows)
df.to_csv("data/raw/api_tweets.csv", index=False)
print("Saved", len(df), "tweets")