import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

IN_PATH = "data/processed/stance_weak.csv"
MODEL_PATH = "models/stance_model.joblib"


# --------------------------------------------------------------------
# 🟦 Balance Dataset (optional but recommended)
# --------------------------------------------------------------------
def balance(df):
    counts = df["stance"].value_counts()
    min_n = counts.min()  # minority count

    df_bal = pd.concat([
        df[df.stance == c].sample(min_n, random_state=42)
        for c in counts.index
    ]).reset_index(drop=True)

    print("\nBalanced class counts:")
    print(df_bal["stance"].value_counts())

    return df_bal


# --------------------------------------------------------------------
# 🟦 Main Training Function
# --------------------------------------------------------------------
def main():
    Path("models").mkdir(exist_ok=True)

    print("Loading dataset...")
    df = pd.read_csv(IN_PATH).dropna(subset=["clean_text", "stance"])
    df["clean_text"] = df["clean_text"].astype(str)

    print("Initial class distribution:")
    print(df["stance"].value_counts())

    # ----------- BALANCE CLASSES -----------
    df_bal = balance(df)

    # ----------- 80/20 TRAIN-TEST SPLIT -----------
    train_df, test_df = train_test_split(
        df_bal,
        test_size=0.2,
        random_state=42,
        stratify=df_bal["stance"]
    )

    print("\nTrain size:", len(train_df))
    print("Test size:", len(test_df))

    Xtr = train_df["clean_text"]
    ytr = train_df["stance"]
    Xv = test_df["clean_text"]
    yv = test_df["stance"]

    # ----------- PIPELINE (TF-IDF + Logistic Regression) -----------
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(
            max_features=60000,
            ngram_range=(1, 2),
            min_df=3,
            stop_words="english",
            sublinear_tf=True
        )),
        ("clf", LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        ))
    ])

    print("\nTraining stance model...")
    pipe.fit(Xtr, ytr)

    # ----------- VALIDATION REPORT -----------
    preds = pipe.predict(Xv)
    print("\nClassification Report:")
    print(classification_report(yv, preds, digits=3))

    # ----------- SAVE MODEL -----------
    joblib.dump(pipe, MODEL_PATH)
    print(f"\nSaved model → {MODEL_PATH}")


# --------------------------------------------------------------------
if __name__ == "__main__":
    main()