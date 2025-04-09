# log.py - Quick test for logging a sample query to AWS RDS

import os
import streamlit as st
from datetime import datetime
import psycopg2
import pandas as pd

def log_query(company, question, answer):
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(
            host=st.secrets["DB_HOST"],
            database=st.secrets["DB_NAME"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            port=st.secrets.get("DB_PORT", 5432)
        )
        cursor = conn.cursor()

        print("Ensuring table exists...")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS query_logs (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                company TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            );
            """
        )
        conn.commit()

        print("Inserting log entry...")
        cursor.execute(
            """
            INSERT INTO query_logs (timestamp, company, question, answer)
            VALUES (%s, %s, %s, %s)
            """,
            (datetime.now(), company, question, answer)
        )
        conn.commit()

        cursor.close()
        conn.close()
        print("Query logged successfully to RDS.")
    except Exception as e:
        print("Failed to log to RDS:", e)



def fetch_recent_logs():
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT", 5432)
        )
        cursor = conn.cursor()

        print("Fetching top 5 logs...")
        cursor.execute("SELECT timestamp, company, question, answer FROM query_logs ORDER BY timestamp DESC LIMIT 5;")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        print("Fetched logs successfully.")
        return rows
    except Exception as e:
        print("Failed to fetch logs from RDS:", e)
        return []

if __name__ == "__main__":
    print("Starting log test...")
    log_query("Tesla", "What’s happening with Tesla lately?", "Tesla has recently seen a dip in stock prices following...")

    print("Recent logs:")
    logs = fetch_recent_logs()
    for log in logs:
        print(log)
