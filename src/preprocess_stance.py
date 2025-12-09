import re
import pandas as pd
from pathlib import Path
from weak_label import weak_label

RAW_PATH = "C:/Users/Bhoomi/ukr_vs_russia_tweets/data/clean/combined.csv"    # adjust if different
OUT_PATH = "data/processed/stance_weak.csv"

def clean_text(s: str) -> str:
    s = str(s).lower()
    s = re.sub(r"http\S+|@\w+", " ", s)
    s = re.sub(r"#(\w+)", r"\1", s)            # keep hashtag word
    s = re.sub(r"[^a-z\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def main():
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(RAW_PATH)
    if "text" not in df.columns:
        raise RuntimeError("Expected a 'text' column in the raw CSV.")
    df = df.dropna(subset=["text"])

    df["clean_text"] = df["text"].apply(clean_text)
    df["stance"] = df["clean_text"].apply(weak_label)

    # keep only what we need
    keep_cols = [c for c in ["id","created_at","text","clean_text","stance"] if c in df.columns]
    df = df[keep_cols]
    df.to_csv(OUT_PATH, index=False)
    print(f"Saved {len(df)} rows → {OUT_PATH}")
    print(df["stance"].value_counts())

if __name__ == "__main__":
    main()