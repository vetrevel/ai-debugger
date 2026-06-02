import json
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Trainer,
    TrainingArguments,
)

MODEL_NAME = "google/flan-t5-small"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading model...")
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

with open("../datasets/debug_dataset.json", "r") as f:
    data = json.load(f)

dataset = Dataset.from_list(data)

def preprocess(example):
    prompt = f"Debug this code:\n{example['buggy_code']}"

    target = (
        f"Fixed Code:\n{example['fixed_code']}\n\n"
        f"Explanation:\n{example['explanation']}"
    )

    model_inputs = tokenizer(
        prompt,
        truncation=True,
        padding="max_length",
        max_length=128,
    )

    labels = tokenizer(
        target,
        truncation=True,
        padding="max_length",
        max_length=128,
    )

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

print("Tokenizing dataset...")
tokenized_dataset = dataset.map(preprocess)

training_args = TrainingArguments(
    output_dir="../models/debug-assistant",
    num_train_epochs=1,
    per_device_train_batch_size=1,
    logging_steps=1,
    save_strategy="no",
    report_to="none",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

print("Starting Training...")
trainer.train()

print("Saving Model...")
trainer.save_model("../models/debug-assistant")

print("Training Complete!")