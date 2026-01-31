import pandas as pd
import os

def check_news_data(filename='../data/raw/news.csv'):
    """
    Checks for missing sentiment scores, data sparsity, and news volume.
    """
    if not os.path.exists(filename):
        print(f"❌ File {filename} not found.")
        return

    # Load data
    df = pd.read_csv(filename)
    
    # Standardize dates (Removing time to check daily coverage)
    df['date_dt'] = pd.to_datetime(df['date'], utc=True)
    df['date_only'] = df['date_dt'].dt.date

    print(f"📊 NEWS DATA INTEGRITY REPORT: {filename}")
    print(f"📅 Period: {df['date_dt'].min().date()} to {df['date_dt'].max().date()}")
    print(f"🔢 Total Headlines: {len(df)}")
    print("=" * 45)

    # 1. Check for Nulls in Sentiment Columns
    print("🔍 NULL ENTRIES PER COLUMN:")
    sentiment_cols = ['sentiment_polarity', 'sentiment_neg', 'sentiment_neu', 'sentiment_pos']
    null_counts = df[sentiment_cols].isnull().sum()
    for col, count in null_counts.items():
        status = "✅ CLEAN" if count == 0 else f"⚠️ {count} MISSING"
        print(f"  {col:20}: {status}")
    print("-" * 45)

    # 2. Check for Data Sparsity (Days without any news)
    # Generate full calendar range based on your Price Data range
    all_days = pd.date_range(start=df['date_only'].min(), end=df['date_only'].max(), freq='D').date
    days_with_news = df['date_only'].unique()
    missing_news_days = [d for d in all_days if d not in days_with_news]
    
    print(f"🗞️ COVERAGE ANALYSIS:")
    print(f"  Total Calendar Days : {len(all_days)}")
    print(f"  Days with News      : {len(days_with_news)}")
    print(f"  Days with NO News   : {len(missing_news_days)}")
    
    # 3. Density Check (Headlines per day)
    avg_headlines = len(df) / len(days_with_news)
    print(f"  Avg Headlines/Day   : {avg_headlines:.2f}")
    
    if avg_headlines < 1:
        print("  ⚠️ WARNING: Low news density may result in weak sentiment signals.")
    else:
        print("  ✅ Density is sufficient for daily aggregation.")
    
    print("=" * 45)

if __name__ == '__main__':
    check_news_data('../data/raw/news.csv')