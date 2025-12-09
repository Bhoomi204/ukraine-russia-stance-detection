import numpy as np
import joblib
from pathlib import Path
import re

MODEL_PATH = Path("models/stance_model.joblib")
THRESH = 0.55  # if max prob < THRESH → neutral

def clean_text(s: str) -> str:
    s = str(s).lower()
    s = re.sub(r"http\S+|@\w+", " ", s)
    s = re.sub(r"#(\w+)", r"\1", s)
    s = re.sub(r"[^a-z\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def predict_stance(texts):
    model = joblib.load(MODEL_PATH)
    clean = [clean_text(t) for t in texts]
    # use proba if available; else fall back to direct predict
    if hasattr(model[-1], "predict_proba"):
        proba = model.predict_proba(clean)
        classes = model.classes_
        outs = []
        for p in proba:
            i = int(np.argmax(p))
            outs.append(classes[i] if p[i] >= THRESH else "neutral")
        return outs
    else:
        return model.predict(clean)

if __name__ == "__main__":
    samples = [
        "Stand with Ukraine!",
        "NATO provoked Russia; Putin is right.",
        "War harms everyone. Ceasefire now."
    ]
    for t, y in zip(samples, predict_stance(samples)):
        print(f"{t} → {y}")