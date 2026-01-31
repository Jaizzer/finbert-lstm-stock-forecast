#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Starting setup for finbert-lstm-stock-forecast..."

# 1. Create Virtual Environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# 2. Activate Environment
echo "🔌 Activating environment..."
source venv/bin/activate

# 3. Upgrade Pip and Install Requirements
echo "📥 Installing dependencies (this may take a minute)..."
pip install --upgrade pip
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found! Installing base packages..."
    pip install yfinance pandas transformers torch tensorflow ipykernel
fi

# 4. Register Jupyter Kernel
echo "🧬 Registering Jupyter Kernel..."
python -m ipykernel install --user --name=finbert-lstm-stock-forecast --display-name "Python (finbert-lstm-stock-forecast)"

# 5. Download Initial Data
if [ -f scripts/download_data.py ]; then
    echo "📊 Downloading price data..."
    python scripts/download-price-data.py
else
    echo "ℹ️ scripts/download-price-data.py not found. Skipping data download."
fi

echo "✅ Setup complete! To start working, run: source venv/bin/activate"