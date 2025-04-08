import streamlit as st
import os

from fetcher import fetch_news
from preprocess import preprocess_news
from sentiment import analyze_sentiment
from embed import embed_articles
from rag_query import ask_question

st.set_page_config(page_title="Financial News Assistant", layout="wide")
st.title("📰 Financial News Assistant")

os.makedirs("./data/raw", exist_ok=True)
os.makedirs("./data/processed", exist_ok=True)

company = st.text_input("Enter a company name to analyze:", "Tesla")

if st.button("Run Pipeline"):
    with st.spinner("Fetching and analyzing news..."):
        fetch_news(company)
        preprocess_news(company)
        analyze_sentiment(company)
        embed_articles(company)
    st.success(f"Pipeline complete for {company}!")

query = st.text_input("Ask a question about the news:")
if st.button("Get Answer") and query:
    with st.spinner("Thinking..."):
        st.markdown("---")
        st.markdown(f"**💬 Answer to '{query}':**")
        answer = ask_question(company, query)
        st.write(answer)
