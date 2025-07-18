# scripts/train_ner.py

import pandas as pd
from datasets import Dataset, ClassLabel, load_metric
from transformers import (
    AutoTokenizer, AutoModelForTokenClassification,
    TrainingArguments, Trainer, DataCollatorForTokenClassification
)
import numpy as np
import torch
import os

# Load labeled data
data_path = "labeled_telegram_product_price_location.txt"

def read_conll_data(filepath):
    sentences, labels = [], []
    current_tokens, current_labels = [], []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == "":
                if current_tokens:
                    sentences.append(current_tokens)
                    labels.append(current_labels)
                    current_tokens, current_labels = [], []
            else:
                parts = line.split()
                if len(parts) >= 2:
                    token, tag = parts[0], parts[-1]
                    current_tokens.append(token)
                    current_labels.append(tag)
    return sentences, labels

tokens, tags = read_conll_data(data_path)
label_list = sorted(list(set(tag for tag_seq in tags for tag in tag_seq)))
label2id = {l: i for i, l in enumerate(label_list)}
id2label = {i: l for l, i in label2id.items()}

def tokenize_and_align_labels(tokenizer, tokens, tags):
    tokenized_inputs = tokenizer(tokens, truncation=True, is_split_into_words=True, padding=True)
    labels = []
    for i, label in enumerate(tags):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:
                label_ids.append(label2id[label[word_idx]])
            else:
                label_ids.append(label2id[label[word_idx]] if label[word_idx].startswith("I-") else label2id[label[word_idx]])
            previous_word_idx = word_idx
        labels.append(label_ids)
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

# Initialize model and tokenizer
model_name = "Davlan/xlm-roberta-base-ner-hrl"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(
    model_name, num_labels=len(label_list), id2label=id2label, label2id=label2id
)

# Prepare dataset
dataset = Dataset.from_dict({"tokens": tokens, "ner_tags": tags})
tokenized_dataset = dataset.map(lambda x: tokenize_and_align_labels(tokenizer, x["tokens"], x["ner_tags"]), batched=True)

# Split
train_test = tokenized_dataset.train_test_split(test_size=0.2)
train_dataset = train_test["train"]
eval_dataset = train_test["test"]

# Data collator
data_collator = DataCollatorForTokenClassification(tokenizer)

# Metric
metric = load_metric("seqeval")
def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    true_labels = [
        [id2label[l] for l in label if l != -100]
        for label in labels
    ]
    true_predictions = [
        [id2label[p] for (p, l) in zip(pred, label) if l != -100]
        for pred, label in zip(predictions, labels)
    ]
    results = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }

# Training setup
training_args = TrainingArguments(
    output_dir="./models/ner-model",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,
    weight_decay=0.01,
    logging_dir="./outputs/logs",
    logging_steps=10,
    save_total_limit=1,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics
)

# Train
trainer.train()

# Save
os.makedirs("models/ner-model", exist_ok=True)
model.save_pretrained("models/ner-model")
tokenizer.save_pretrained("models/ner-model")

print("✅ Model training complete and saved.")
