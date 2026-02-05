import pandas as pd
import os
import numpy as np

def intersect_by_density():
    # 1. Paths
    price_file = '../data/raw/prices.csv'
    sentiment_file = '../data/processed/daily_news_sentiment.csv'
    output_file = '../data/processed/intersect_dense_data.csv'

    # 2. Load Data
    prices = pd.read_csv(price_file)
    sent = pd.read_csv(sentiment_file)
    
    prices['Date'] = pd.to_datetime(prices['Date'])
    sent['date'] = pd.to_datetime(sent['date'])

    # 3. Define Gold Range (Temporal bounds based on news density analysis)
    start_date = pd.to_datetime('2020-11-23')
    end_date = pd.to_datetime('2024-11-27')
    
    print(f"🎯 Master Anchor: Price Data")
    print(f"📏 Clipping to Gold Cluster: {start_date.date()} to {end_date.date()}")

    # 4. Clipping Price Data (Primary Anchor for Trading Days)
    mask = (prices['Date'] >= start_date) & (prices['Date'] <= end_date)
    prices_clipped = prices.loc[mask].copy().sort_values('Date')

    # 5. Temporal Alignment: Roll Non-Trading Day News Forward
    # Captures weekend/holiday sentiment and assigns it to the next open market session
    print("🔄 Propagating weekend/holiday news to next trading day...")
    
    # Create reference series for available exchange dates
    trading_days = prices_clipped[['Date']].copy().rename(columns={'Date': 'Trading_Date'}).sort_values('Trading_Date')
    
    sent = sent.sort_values('date')
    
    # Use asynchronous join to map news timestamps to the nearest future trading date
    sent_rolled = pd.merge_asof(
        sent, 
        trading_days, 
        left_on='date', 
        right_on='Trading_Date', 
        direction='forward'
    )

    # 6. Aggregate Sentiment by Target Trading Date
    # Averages multiple headlines (e.g., Sat + Sun + Mon) into a single daily signal
    sent_grouped = sent_rolled.groupby('Trading_Date').agg({
        'sentiment_pos': 'mean',
        'sentiment_neg': 'mean',
        'sentiment_neu': 'mean',
        'net_sentiment': 'mean'
    }).reset_index()

    # 7. Feature Integration
    # Merge price anchor with aggregated sentiment signals
    final_df = pd.merge(prices_clipped, sent_grouped, left_on='Date', right_on='Trading_Date', how='left')

    # 8. Imputation of Sparse Signals
    # Assign neutral sentiment weights to trading days lacking specific headline coverage
    print("🛠️ Applying Neutral Imputation for days with zero news coverage...")
    final_df['sentiment_neu'] = final_df['sentiment_neu'].fillna(1.0)
    cols_to_zero = ['sentiment_pos', 'sentiment_neg', 'net_sentiment']
    final_df[cols_to_zero] = final_df[cols_to_zero].fillna(0.0)

    # 9. Target Engineering (Logarithmic Returns)
    if 'Trading_Date' in final_df.columns:
        final_df = final_df.drop(columns=['Trading_Date'])
    
    final_df = final_df.sort_values('Date')
    
    # Calculate daily log-returns for stationarity: ln(Price_t / Price_t-1)
    final_df['Target_Return'] = np.log(final_df['Close'] / final_df['Close'].shift(1))    
    
    # Remove initial observation (NaN return) to maintain sequence integrity
    final_df = final_df.dropna() 

    # 10. Persist Processed Dataset
    os.makedirs('../data/processed', exist_ok=True)
    final_df.to_csv(output_file, index=False)

    print(f"✅ Intersection Complete!")
    print(f"📊 Final Dataset Shape: {final_df.shape}")
    print(f"📅 Inclusive Dates: {final_df['Date'].min().date()} to {final_df['Date'].max().date()}")

if __name__ == "__main__":
    intersect_by_density()