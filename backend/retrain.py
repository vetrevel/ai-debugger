import json
from datetime import datetime
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Trainer,
    TrainingArguments
)

MODEL_NAME = "google/flan-t5-small"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading model...")
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# Load dataset
with open("../datasets/debug_dataset.json", "r") as f:
    data = json.load(f)

print(f"Loaded {len(data)} examples")

dataset = Dataset.from_list(data)

def preprocess(example):
    prompt = f"""
Debug this code:

{example['buggy_code']}
"""

    target = f"""
Fixed Code:
{example['fixed_code']}

Explanation:
{example['explanation']}
"""

    model_inputs = tokenizer(
        prompt,
        truncation=True,
        padding="max_length",
        max_length=128
    )

    labels = tokenizer(
        target,
        truncation=True,
        padding="max_length",
        max_length=128
    )

    model_inputs["labels"] = labels["input_ids"]

    return model_inputs

print("Tokenizing dataset...")
tokenized_dataset = dataset.map(preprocess)

version = datetime.now().strftime("%Y%m%d_%H%M%S")

save_path = f"../models/model_{version}"

training_args = TrainingArguments(
    output_dir=save_path,
    num_train_epochs=5,
    per_device_train_batch_size=2,
    logging_steps=10,
    save_strategy="epoch",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset
)

print("Starting retraining...")
trainer.train()

print("Saving model...")
trainer.save_model(save_path)

print(f"Model saved to: {save_path}")