
from fetcher import fetch_news
from preprocess import preprocess_news
from sentiment import analyze_sentiment
from embed import embed_articles
from rag_query import ask_question


if __name__ == "__main__":
    company = input("Enter company name: ")
    fetch_news(company)
    preprocess_news(company)
    analyze_sentiment(company)
    embed_articles(company)

    query = input("Ask a question about the news: ")
    ask_question(company, query)

