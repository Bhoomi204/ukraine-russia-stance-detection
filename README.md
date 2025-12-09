# Ukraine–Russia Twitter Stance Detection (NLP Project)
## 🔥 A Machine Learning Pipeline to Classify Tweets as:

-Pro-Ukraine

-Pro-Russia

-Neutral

This project demonstrates end-to-end NLP, including live tweet extraction, preprocessing, dataset balancing, stance classification, and model evaluation.

## 🚀 1. Project Overview

This project analyzes real tweets related to the Ukraine–Russia conflict to determine public stance.

It covers:

-Tweet extraction (API + SNScrape hybrid)

-Text cleaning & preprocessing

-Automatic stance labeling using keyword heuristics

-Class imbalance correction

-Train/test split (80–20 stratified)

-TF-IDF vectorization

-Logistic Regression classifier

-Model evaluation

-Prediction on new, unseen tweets

## 📁 2. Folder Structure
project/

│

├── data/

│   ├── raw/              # Extracted tweets

│   ├── processed/        # Cleaned + labeled data

│

├── src/

│   ├── fetch_tweets.py       # API extraction

│   ├── extract_tweets.py     # SNScrape extraction

│   ├── combine_datasets.py   # Merge API + SNScrape data

│   ├── preprocess_stance.py  # Cleaning + stance labeling

│   ├── train_stance.py       # Model training

│   ├── predict_stance.py     # Predict on new tweets

│

├── models/

│   ├── stance_model.joblib

│

├── requirements.txt

└── README.md

## 🧵 3. Installation

Clone the repo:

git clone https://github.com/username/ukraine-russia-stance-detection
cd ukraine-russia-stance-detection


Create virtual environment:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

## 🐦 4. Extracting Tweets
### (A) SNScrape (No API required)
python src/extract_tweets.py

### (B) Twitter API (Bearer Token Required)
setx TWITTER_BEARER_TOKEN "YOUR_TOKEN"
python src/fetch_tweets.py


Provides 100 fresh tweets per run.

## 🧹 5. Preprocessing & Labeling
python src/preprocess_stance.py


Tasks performed:

-Remove duplicates

-Clean URLs, hashtags, emojis

-Apply keyword-based weak labeling

-Normalize stance classes

## 🎯 6. Training the Model
python src/train_stance.py


Includes:

-TF-IDF vectorization

-Logistic Regression

-Balanced classes

-80–20 stratified train-test split

Example model performance:

Class	F1 Score
Neutral	0.83
Pro-Russia	0.94
Pro-Ukraine	0.91

## 🔮 7. Predict on New Tweets
python src/predict_stance.py

## 📊 8. Why Logistic Regression?

-Fast and interpretable

-Works extremely well with high-dimensional sparse data (TF-IDF)

-Outperforms SVM when dataset is large

-Much cheaper computationally than transformer-based models

## ⭐ 9. Unique Contributions (Your Original Work)

-Built a hybrid dataset from API + SNScrape

-Created weak supervision rules to assign political stances

-Solved extreme class imbalance using heuristic resampling

-Implemented auto-column detection to merge heterogeneous datasets

-Full end-to-end automated pipeline

-Added stratified split to ensure fair testing

## 📝 10. Future Improvements

-Use BERT/RoBERTa for stance detection

-Add sarcasm detection

-Add temporal trend analysis

-Deploy as a web dashboard
