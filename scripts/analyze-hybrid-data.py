import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_hybrid_analysis():
    # 1. Load the data
    price_path = '../data/raw/prices.csv'
    news_path = '../data/processed/daily_news_sentiment.csv'
    
    if not os.path.exists(price_path) or not os.path.exists(news_path):
        print("⚠️ Ensure your prices.csv and daily_news_sentiment.csv are in the correct folders.")
        return

    prices = pd.read_csv(price_path)
    news = pd.read_csv(news_path)

    # 2. Synchronize Dates
    prices['Date'] = pd.to_datetime(prices['Date']).dt.date
    news['date'] = pd.to_datetime(news['date']).dt.date

    # 3. Create the Intersection (Inner Join)
    # This aligns the daily sentiment average with that day's price
    df = pd.merge(prices, news, left_on='Date', right_on='date', how='inner')
    df = df.drop(columns=['date']).sort_values('Date')

    # 4. Feature Engineering for Analysis
    df['Daily_Return'] = df['Close'].pct_change() * 100 # % Change in price
    df = df.dropna()

    print("="*50)
    print("📈 HYBRID DATASET SUMMARY")
    print(f"Total Synchronized Days: {len(df)}")
    print(f"Date Range: {df['Date'].min()} to {df['Date'].max()}")
    print("="*50)

    # 5. Correlation Analysis
    # We check if Net Sentiment (Pos - Neg) correlates with Price Returns
    correlations = df[['Daily_Return', 'net_sentiment', 'sentiment_pos', 'sentiment_neg', 'Volume']].corr()
    
    print("\n🔍 CORRELATION MATRIX (Pearson):")
    print(correlations['Daily_Return'].sort_values(ascending=False))
    
    # 6. Lag Analysis (Crucial for Prediction)
    # Does news TODAY predict price TOMORROW?
    df['next_day_return'] = df['Daily_Return'].shift(-1)
    lag_corr = df['net_sentiment'].corr(df['next_day_return'])
    print(f"\n🕒 Predictive Lag Correlation (Sentiment vs Next Day Return): {lag_corr:.4f}")

    # 7. Visualizing the Signal
    plt.figure(figsize=(12, 6))
    sns.regplot(x='net_sentiment', y='Daily_Return', data=df, scatter_kws={'alpha':0.3}, line_kws={'color':'red'})
    plt.title('Apple: Daily Net Sentiment vs. Stock Returns')
    plt.xlabel('FinBERT Net Sentiment (Positive - Negative)')
    plt.ylabel('Daily Price Return (%)')
    plt.savefig('data/processed/sentiment_correlation_plot.png')
    
    print("\n✅ Analysis complete. Chart saved to data/processed/sentiment_correlation_plot.png")

if __name__ == "__main__":
    run_hybrid_analysis()