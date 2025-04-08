import os
import requests
import json
from datetime import datetime, timedelta

# Load API key from .env
from dotenv import load_dotenv
load_dotenv("ini.env")

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

def fetch_news(company, days_back=7, page_size=50):
    """
    Fetch recent news articles about the given company from NewsAPI.
    """
    from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    params = {
        "q": company,
        "from": from_date,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": page_size,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    os.makedirs("./data/raw", exist_ok=True)
    filename = f"data/raw/{company.lower().replace(' ', '_')}_news.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Fetched and saved {len(data.get('articles', []))} articles for {company}.")

