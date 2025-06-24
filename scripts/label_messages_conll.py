import pandas as pd
import re
import os

# Load cleaned telegram messages
data_path = "data/processed/telegram_messages_clean.csv"
df = pd.read_csv(data_path)

# We assume the 'Message' column contains the text to label
messages = df['Message'].dropna().tolist()

# Sample lists of keywords (expand these for better coverage)
product_keywords = {
    "silicon", "brush", "spatulas", "mandoline", "slicer",
    "bottle", "warmer", "table", "desk", "edge", "guard", "strip",
    "baby", "milk", "warmers", "thermos", "cup", "holder"
}

# Known locations in Amharic (add more as needed)
locations = {
    "አዲስ", "አበባ", "ቦሌ", "ጎንደር", "ሐረር", "ሐዋርያ", "አምባሳዬ"
}

# Regex to find prices (numbers followed by ብር)
price_pattern = re.compile(r'\d+\s*ብር')

def label_tokens(message):
    tokens = message.split()
    labels = []

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Check price pattern in next 1 or 2 tokens combined
        window = ' '.join(tokens[i:i+2])
        if price_pattern.search(window):
            price_tokens = window.split()
            for j, pt in enumerate(price_tokens):
                label = "B-PRICE" if j == 0 else "I-PRICE"
                labels.append((pt, label))
            i += len(price_tokens)
            continue

        # Check for product keywords
        if token.lower() in product_keywords:
            labels.append((token, "B-PRODUCT"))
            k = i + 1
            # Label following tokens also as I-PRODUCT if they are product keywords
            while k < len(tokens) and tokens[k].lower() in product_keywords:
                labels.append((tokens[k], "I-PRODUCT"))
                k += 1
            i = k
            continue

        # Check for locations
        # Also check if current and next token form a location (e.g. አዲስ አበባ)
        if token in locations:
            if i + 1 < len(tokens) and tokens[i+1] in locations:
                labels.append((token, "B-LOC"))
                labels.append((tokens[i+1], "I-LOC"))
                i += 2
                continue
            else:
                labels.append((token, "B-LOC"))
                i += 1
                continue

        # Otherwise label as O
        labels.append((token, "O"))
        i += 1

    return labels

# Output file for CoNLL format
output_file = "labeled_telegram_product_price_location.txt"

with open(output_file, "w", encoding="utf-8") as f:
    for msg in messages[:50]:  # label first 50 messages as per your requirement
        labeled = label_tokens(msg)
        for token, label in labeled:
            f.write(f"{token} {label}\n")
        f.write("\n")  # blank line to separate messages

print(f"Labeled {min(50,len(messages))} messages saved to {output_file}")
