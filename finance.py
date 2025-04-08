import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(ticker, days_back=7):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days_back)

    df = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    if df.empty:
        print(f"No stock data found for ticker: {ticker}")
        return

    df.reset_index(inplace=True)
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    os.makedirs("data/finance", exist_ok=True)
    df.to_parquet(f"data/finance/{ticker.lower()}_price.parquet", index=False)

    print(f"Fetched and saved stock price data for {ticker}.")
    return file_path


if __name__ == "__main__":
    ticker = input("Enter stock ticker (e.g. TSLA): ")
    fetch_stock_data(ticker)
