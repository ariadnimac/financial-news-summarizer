# financial-news-summarizer

This project is a Streamlit-based application that allows users to query and summarise recent financial news related to a selected company. It combines unstructured text data from news sources with structured stock price information to provide clear, context-aware responses using a Retrieval-Augmented Generation (RAG) approach.

## Features
1. Fetches recent news articles using NewsAPI based on a company name

2. Cleans and preprocesses the articles

3. Applies sentiment analysis to assess tone

4. Embeds articles using OpenAI embeddings

5. Stores embeddings in FAISS for semantic search

6. Allows users to ask questions about the news and receive summarised answers

7. Displays recent stock price trends from Yahoo Finance

8. Logs each question, answer, and timestamp to a PostgreSQL database (AWS RDS)

## Streamlit Application
The frontend is built using Streamlit, providing a lightweight and interactive interface. Users can input a company name, run the full pipeline, ask questions, and view historical logs of queries directly within the app.

## Project Structure
/
- fetcher.py           # Fetches news articles using NewsAPI
- preprocess.py        # Cleans and filters raw news data
- sentiment.py         # Applies sentiment analysis (VADER or OpenAI)
- embed.py             # Embeds articles using OpenAI and stores in FAISS
- rag_query.py         # Handles question-answering using RAG
- finance.py           # Retrieves stock price data and maps company to ticker
- dashboard.py         # Streamlit application interface
- log.py               # Logs user queries and fetches past entries from RDS

data/
- raw/                 # Raw news JSON files
- processed/           # Cleaned and embedded files (JSON, Parquet, FAISS)
- finance/             # Stock price data in Parquet format
- logs/                # Optional local query logs (if not using RDS)

- requirements.txt       # Python package dependencies

## Deployment Notes
- All environment variables are stored using secrets.toml when deployed on Streamlit Cloud.
- The PostgreSQL logging system uses Amazon RDS, and the table query_logs is created automatically if it does not exist.
