import pandas as pd

df = pd.read_csv("data/raw/ukraine_russia_war_tweets.csv")
print(df.columns)
print(df.head())