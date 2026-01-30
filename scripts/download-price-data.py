import yfinance as yf
import pandas as pd
import os

def download_data():
    TICKER = "AAPL"
    # Ensure end_date is formatted correctly
    df = yf.download(TICKER, start="2015-01-01", end="2026-01-29", auto_adjust=True)

    # 1. Check if we actually got data
    if df.empty:
        print("❌ Error: Downloaded DataFrame is empty. Check your internet or Ticker.")
        return

    # 2. Fix the MultiIndex (The "Blank File" Culprit)
    # Modern yfinance often returns columns like ('Close', 'AAPL')
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0) # Keep 'Close', drop 'AAPL'

    df.reset_index(inplace=True)

    # 3. Save with an Absolute-style path to be safe
    # This points one level up from /scripts and into /data/raw
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", "data", "raw", "prices.csv")
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)
    
    print(f"✅ Success! Saved {len(df)} rows to {file_path}")
    print(df.head()) # Preview the data in terminal

if __name__ == "__main__":
    download_data()