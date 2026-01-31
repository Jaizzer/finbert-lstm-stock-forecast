import kagglehub
import pandas as pd
import os

def download_news():
    print("🚀 Downloading AAPL News Dataset via kagglehub...")
    
    # This downloads the dataset and returns the local directory path
    path = kagglehub.dataset_download("frankossai/apple-stock-aapl-historical-financial-news-data")
    
    # The file in this specific dataset is named 'apple_news_data.csv'
    source_file = os.path.join(path, "apple_news_data.csv")
    target_file = "data/raw/news.csv"
    
    if os.path.exists(source_file):
        df = pd.read_csv(source_file)
        
        # Create directory if it doesn't exist
        os.makedirs("data/raw", exist_ok=True)
        
        # Save to your project structure
        df.to_csv(target_file, index=False)
        print(f"✅ Success! Saved {len(df)} rows to {target_file}")
    else:
        print("❌ Error: Could not find the CSV in the downloaded bundle.")

if __name__ == "__main__":
    download_news()