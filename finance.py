import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

TICKER_MAP = {
    "tesla": "TSLA",
    "apple": "AAPL",
    "microsoft": "MSFT",
    "amazon": "AMZN",
    "google": "GOOGL",
    "meta": "META",
    "nvidia": "NVDA",
    "intel": "INTC",
    "netflix": "NFLX",
    "facebook": "META"
}

def get_ticker_from_name(company_name):
    return TICKER_MAP.get(company_name.strip().lower(), "")

def fetch_stock_data(ticker, days_back=7):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days_back)

    df = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    print("🔍 Raw DataFrame columns returned by yfinance:")
    print(df.columns)
    if df is None or df.empty:
        print(f"No stock data found for ticker: {ticker}")
        return None

    df.reset_index(inplace=True)
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    os.makedirs("data/finance", exist_ok=True)
    file_path = f"data/finance/{ticker.lower()}_price.parquet"
    df.to_parquet(file_path, index=False)

    print(f"Fetched and saved stock price data for {ticker}.")
    return file_path

if __name__ == "__main__":
    ticker = input("Enter stock ticker (e.g. TSLA): ")
    fetch_stock_data(ticker)
