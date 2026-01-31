import pandas as pd
import os

def check_missing_price_data(filename='../data/raw/prices.csv'):
    """
    Checks for NaN values, duplicate dates, and business day gaps in price data.
    """
    if not os.path.exists(filename):
        print(f"❌ File {filename} not found. Check your path.")
        return

    # Load data
    df = pd.read_csv(filename)
    
    # Standardize dates
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    print(f"📊 DATA INTEGRITY REPORT: {filename}")
    print(f"📅 Period: {df['Date'].min().date()} to {df['Date'].max().date()}")
    print(f"🔢 Total Records: {len(df)}")
    print("=" * 40)

    # 1. Check for Nulls (NaNs) in specific entries
    print("🔍 NULL ENTRIES PER COLUMN:")
    null_counts = df.isnull().sum()
    for col, count in null_counts.items():
        status = "✅ CLEAN" if count == 0 else f"⚠️ {count} MISSING"
        print(f"  {col:10}: {status}")
    print("-" * 40)

    # 2. Check for Duplicate Dates
    # In stock data, one date should have exactly one row.
    duplicates = df[df['Date'].duplicated()]
    if not duplicates.empty:
        print(f"⚠️ DUPLICATE DATES FOUND: {len(duplicates)}")
        print(duplicates['Date'].head())
    else:
        print("✅ NO DUPLICATE DATES FOUND")
    print("-" * 40)

    # 3. Check for Market Gaps (Business Days only)
    # freq='B' generates a range of all weekdays (Mon-Fri)
    expected_range = pd.date_range(start=df['Date'].min(), end=df['Date'].max(), freq='B')
    missing_days = expected_range.difference(df['Date'])
    
    print(f"🕳️ MISSING MARKET DAYS (Gaps in sequence): {len(missing_days)}")
    if len(missing_days) > 0:
        print("  Top 5 missing business dates:")
        for d in missing_days[:5]:
            print(f"    - {d.date()}")
    else:
        print("✅ DATA IS CONTINUOUS (No gaps)")
    
    print("=" * 40)

if __name__ == '__main__':
    # You can change the path here if your file is named differently
    check_missing_price_data('../data/raw/prices.csv')