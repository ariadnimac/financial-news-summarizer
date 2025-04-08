import os
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download("vader_lexicon")

def analyze_sentiment(company):
    input_path = f"data/processed/{company.lower().replace(' ', '_')}_cleaned.json"
    output_path = f"data/processed/{company.lower().replace(' ', '_')}_scored.json"

    with open(input_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    sid = SentimentIntensityAnalyzer()

    for article in articles:
        content = article.get("content", "")
        score = sid.polarity_scores(content)
        article["sentiment"] = score

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2)

    print(f"Sentiment scored and saved for {len(articles)} articles about {company}.")

if __name__ == "__main__":
    company = input("Enter company name to score sentiment: ")
    analyze_sentiment(company)
