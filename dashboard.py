import streamlit as st

from fetcher import fetch_news
from preprocess import preprocess_news
from sentiment import analyze_sentiment
from embed import embed_articles
from rag_query import ask_question
from finance import fetch_stock_data

def get_ticker_from_name(company_name):
    url = f"https://query1.finance.yahoo.com/v1/finance/search?q={company_name}"
    try:
        response = requests.get(url)
        results = response.json()
        if results.get("quotes"):
            return results["quotes"][0].get("symbol", "")
    except Exception as e:
        print("Error retrieving ticker:", e)
    return ""

st.set_page_config(page_title="Financial News Assistant", layout="wide")
st.title("📰 Financial News Assistant")

company = st.text_input("Enter a company name to analyse:", "Tesla")
auto_ticker = get_ticker_from_name(company)

if st.button("Run Pipeline"):
    with st.spinner("Fetching and analyzing news..."):
        fetch_news(company)
        preprocess_news(company)
        analyze_sentiment(company)
        embed_articles(company)
        stock_file = fetch_stock_data(ticker)

    st.success(f"Pipeline complete for {company}!")
    if stock_file:
        st.subheader("📈 Stock Price Overview")
        df_stock = pd.read_parquet(stock_file)
        fig = px.line(df_stock, x='Date', y='Close', title=f"{ticker} Closing Price (Last 7 Days)")
        st.plotly_chart(fig, use_container_width=True)

query = st.text_input("Ask a question about the news:")
if st.button("Get Answer") and query:
    with st.spinner("Thinking..."):
        st.markdown("---")
        st.markdown(f"**💬 Answer to '{query}':**")
        answer = ask_question(company, query)
        st.write(answer)
