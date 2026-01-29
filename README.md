# Hybrid Stock Return Prediction: LSTM + FinBERT Sentiment

## Overview
This project implements a hybrid deep learning approach for predicting daily **stock log returns** by combining:

- **LSTM networks** for time-series modeling of historical stock data  
- **FinBERT-based sentiment analysis** for extracting insights from financial news

The goal is to improve predictive accuracy by leveraging both quantitative and qualitative features.

---

## Project Structure
    finbert-lstm-stock-forecast/
    ├── data/
    │   ├── raw/         # Original datasets (prices.csv, news.csv)
    │   └── processed/   # Cleaned and feature-engineered data
    ├── models/
    │   ├── lstm.py      # LSTM architecture and training functions
    │   └── finbert.py   # FinBERT-based sentiment feature extraction
    ├── notebooks/
    │   ├── 01_preprocessing.ipynb
    │   └── 02_training.ipynb
    ├── configs/
    │   └── config.yaml  # Hyperparameters and file paths
    ├── scripts/         # Optional utility scripts
    ├── requirements.txt
    └── README.md

---

## Data

- **prices.csv**: Daily historical stock prices including `Open`, `High`, `Low`, `Close`, `Volume`  
- **news.csv**: Daily financial news headlines  
- **Processed data**: Includes log returns, technical indicators, and aggregated sentiment features  

> Note: Only publicly available data is used to ensure reproducibility.

---

## Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd project_root
    ```

2. Create a virtual environment and install dependencies
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
