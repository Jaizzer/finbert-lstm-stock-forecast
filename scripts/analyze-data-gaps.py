import pandas as pd

def analyze_date_gaps(filename='../data/processed/daily_news_sentiment.csv'):
    # 1. Load data
    df = pd.read_csv(filename)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    # 2. Calculate the gap in days between current and previous row
    df['gap_days'] = df['date'].diff().dt.days

    print("="*50)
    print("📅 SENTIMENT DATA GAP ANALYSIS")
    print("="*50)

    # 3. Define thresholds
    # Small gap: <= 3 days (Standard weekend/holiday)
    # Medium gap: 4-7 days
    # Large gap: > 7 days
    small = df[df['gap_days'] <= 3]
    medium = df[(df['gap_days'] > 3) & (df['gap_days'] <= 7)]
    large = df[df['gap_days'] > 7]

    print(f"✅ Healthy/Weekend Gaps (<=3 days): {len(small)}")
    print(f"⚠️ Medium Gaps (4-7 days): {len(medium)}")
    print(f"🚨 Large/Broken Gaps (>7 days): {len(large)}")
    print("-" * 50)

    # 4. Identify the "Best" Continuous Ranges
    # We look for clusters where gaps stay small
    print("💡 DETECTED DENSE DATA CLUSTERS (Gaps <= 7 days):")
    
    clusters = []
    current_start = df['date'].iloc[0]
    
    for i in range(1, len(df)):
        if df['gap_days'].iloc[i] > 7:
            # End of a cluster
            clusters.append((current_start, df['date'].iloc[i-1]))
            current_start = df['date'].iloc[i]
    
    # Add the last cluster
    clusters.append((current_start, df['date'].iloc[-1]))

    # Filter for clusters longer than 30 days for LSTM usability
    for start, end in clusters:
        duration = (end - start).days
        if duration > 30:
            print(f"🚀 Found Cluster: {start.date()} to {end.date()} ({duration} days)")
        else:
            print(f"🌑 Sparse Island: {start.date()} to {end.date()} (Too short)")

if __name__ == "__main__":
    analyze_date_gaps('../data/processed/daily_news_sentiment.csv')