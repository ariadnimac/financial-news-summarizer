import os
import json

def preprocess_news(company):
    """
    Load raw news data, clean it, and save structured output.
    """
    raw_path = f"./data/raw/{company.lower().replace(' ', '_')}_news.json"
    processed_path = f"./data/processed/{company.lower().replace(' ', '_')}_cleaned.json"

    with open(raw_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    articles = raw_data.get("articles", [])
    cleaned_articles = []
    seen = set()

    for article in articles:
        title = article.get("title", "")
        content = article.get("content", "")
        url = article.get("url", "")
        published_at = article.get("publishedAt", "")
        description = article.get("description", "")
        source = article.get("source", {}).get("name", "")

        # Filter out duplicates and missing content
        if not content or url in seen:
            continue

        seen.add(url)
        cleaned_articles.append({
            "title": title,
            "description": description,
            "content": content,
            "published_at": published_at,
            "url": url,
            "source": source
        })

    os.makedirs("data/processed", exist_ok=True)
    with open(processed_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_articles, f, indent=2)

    print(f"Processed and saved {len(cleaned_articles)} cleaned articles for {company}.")
