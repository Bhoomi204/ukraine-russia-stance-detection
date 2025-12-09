import pandas as pd
import os
from pathlib import Path

def main():

    sns_path = "C:/Users/Bhoomi/ukr_vs_russia_tweets/data/raw/ukraine_russia_war_tweets.csv"
    api_path = "data/raw/api_tweets.csv"
    out_path = "data/clean/combined.csv"

    Path("data/clean").mkdir(parents=True, exist_ok=True)

    # ---- Load SNScrape dataset safely ----
    if os.path.exists(sns_path):
        df_sns = pd.read_csv(sns_path)
        print("SNScrape tweets:", len(df_sns))

        possible_text_cols = ["content", "renderedContent", "text"]
        text_col = next((c for c in possible_text_cols if c in df_sns.columns), None)

        if text_col is None:
            raise ValueError("❌ No text column found in SNScrape file!")

        possible_id_cols = ["id", "tweetId", "tweet_id"]
        id_col = next((c for c in possible_id_cols if c in df_sns.columns), None)

        if id_col is None:
            df_sns["id"] = range(1, len(df_sns) + 1)
            id_col = "id"

        possible_date_cols = ["date", "timestamp", "created_at"]
        date_col = next((c for c in possible_date_cols if c in df_sns.columns), None)

        if date_col is None:
            df_sns["date"] = ""
            date_col = "date"

        df_sns = df_sns.rename(columns={
            text_col: "text",
            id_col: "id",
            date_col: "date"
        })

        df_sns = df_sns[["id", "text", "date"]]
        df_sns["source"] = "snscrape"

    else:
        print("SNScrape file missing, skipping...")
        df_sns = pd.DataFrame(columns=["id", "text", "date", "source"])


    # ---- Load API dataset safely ----
    if os.path.exists(api_path):
        df_api = pd.read_csv(api_path)
        print("API tweets:", len(df_api))

        df_api = df_api.rename(columns={
            "id": "id",
            "text": "text",
            "created_at": "date"
        })

        df_api["source"] = "api"

    else:
        print("API file missing, skipping...")
        df_api = pd.DataFrame(columns=["id", "text", "date", "source"])

    # ---- Combine ----
    df = pd.concat([df_sns, df_api], ignore_index=True)
    df.drop_duplicates(subset="text", inplace=True)

    print("Final combined dataset:", len(df))

    df.to_csv(out_path, index=False)
    print("Saved →", out_path)


if __name__ == "__main__":
    main()