# EthioMart: Building an Amharic E-commerce Data Extractor

## Project Summary

EthioMart is a unified platform for e-commerce activities on Telegram in Ethiopia. It identifies key entities—such as products, prices, and locations—from Amharic Telegram channels. This repository contains a complete Amharic Named Entity Recognition (NER) system, including data extraction, model development, and business insights generation.

## Core Features

- **Telegram Data Extraction:** Automated collection and cleaning of Amharic commerce messages.
- **Multilingual NER Models:** Fine-tuned transformer models (XLM-Roberta, mBERT, DistilBERT) for Amharic entity recognition.
- **Business Insights:** Scoring system to support micro-lending decisions.
- **Model Transparency:** SHAP and LIME for explainable AI outputs.

## Repository Layout

```
├── datasets/                # Raw and cleaned data
├── trained_models/          # Pretrained and fine-tuned NER models
├── analysis/                # Jupyter notebooks for workflows
├── utils/                   # Python utility scripts
├── dependencies.txt         # Required Python packages
└── EthioMart_NER_Doc.pdf    # Detailed project documentation
```

## Setup Instructions

### Requirements

- Python 3.8 or higher
- PowerShell (for Windows users)
- NVIDIA GPU (optional, for faster model training)

### Installation Steps

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/EthioMart-NER-System.git
   cd EthioMart-NER-System
   ```

2. **Set up a virtual environment:**

   ```sh
   python -m venv emart-venv
   source emart-venv/bin/activate  # On Windows: .\emart-venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```sh
   pip install -r dependencies.txt
   ```

4. **Create a `.env` file with Telegram API keys:**
   ```
   TELEGRAM_API_KEY=your_api_key
   TELEGRAM_API_SECRET=your_api_secret
   ```

## Usage Guide

### Collecting Data

Run the Telegram data scraper:

```sh
python utils/telegram_collector.py
```

### Preprocessing Data

Clean and format raw data:

```sh
python utils/data_cleaner.py datasets/raw/telegram_data_*.json
```

### Model Training

Run the following notebooks sequentially:

- `analysis/01_data_gathering.ipynb`
- `analysis/02_data_cleaning.ipynb`
- `analysis/03_model_development.ipynb`

### Generating Business Insights

Execute the analytics script:

```sh
python utils/business_scorer.py
```

## Performance Results

| Model       | Precision | Recall | F1-Score | Inference Speed (ms/sample) |
| ----------- | --------- | ------ | -------- | --------------------------- |
| XLM-Roberta | 0.90      | 0.88   | 0.89     | 115                         |
| mBERT       | 0.85      | 0.85   | 0.85     | 145                         |
| DistilBERT  | 0.83      | 0.81   | 0.82     | 70                          |

## Task Breakdown

- Built a reliable scraper for Amharic e-commerce messages.
- Created preprocessing tools to tokenize and clean Telegram JSON data into CSV for training.
- Managed media metadata (e.g., images, files) for efficient processing.
- Excluded `.session` files from version control for security.

## Credits

- Hugging Face for providing transformer models
- Telegram API team
- Amharic NLP research community
