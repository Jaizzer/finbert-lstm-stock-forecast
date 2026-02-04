import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm
import os

def run_finbert_on_news():
    # 1. Paths
    input_file = '../data/raw/news.csv'
    output_file = '../data/processed/daily_news_sentiment.csv'
    
    if not os.path.exists(input_file):
        print(f"❌ {input_file} not found!")
        return

    # 2. Device Setup
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        print("🚀 Using Apple Silicon (MPS) acceleration!")
    else:
        device = torch.device("cpu")
        print("⚠️ Using CPU (inference will take longer)")

    # 3. Load Model
    print("⏳ Loading ProsusAI/finbert...")
    model_name = "ProsusAI/finbert"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)

    # 4. Load & Clean Data
    df = pd.read_csv(input_file)
    
    # Standardize dates for grouping
    df['date'] = pd.to_datetime(df['date'], utc=True).dt.date
    
    # Remove existing sentiment columns to overwrite them
    cols_to_drop = ['sentiment_polarity', 'sentiment_neg', 'sentiment_neu', 'sentiment_pos']
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    
    headlines = df['title'].astype(str).tolist()

    # 5. Batch Processing (The AI Inference)
    batch_size = 64
    all_probs = []

    print(f"🧠 Processing {len(headlines)} headlines...")
    for i in tqdm(range(0, len(headlines), batch_size)):
        batch = headlines[i:i + batch_size]
        inputs = tokenizer(batch, padding=True, truncation=True, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            all_probs.append(probs.cpu())

    # 6. Assign Results back to DataFrame
    results = torch.cat(all_probs).numpy()
    df['sentiment_pos'] = results[:, 0]
    df['sentiment_neg'] = results[:, 1]
    df['sentiment_neu'] = results[:, 2]

    # 7. DAILY AGGREGATION (Averaging multiple news in one day)
    print("🧹 Averaging multiple headlines per day...")
    # Calculate Net Sentiment first (Standard in Financial Research)
    df['net_sentiment'] = df['sentiment_pos'] - df['sentiment_neg']
    
    # Group by date and calculate mean for all sentiment columns
    daily_df = df.groupby('date').agg({
        'sentiment_pos': 'mean',
        'sentiment_neg': 'mean',
        'sentiment_neu': 'mean',
        'net_sentiment': 'mean'
    }).reset_index()

    # 8. Save Final Processed Data
    os.makedirs('../data/processed', exist_ok=True)
    daily_df.to_csv(output_file, index=False)
    
    print(f"✅ Success! Daily aggregated results saved to {output_file}")
    print(f"📊 Final Dataset Shape: {daily_df.shape}")

if __name__ == "__main__":
    run_finbert_on_news()