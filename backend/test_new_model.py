from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_PATH = "../models/model_20260601_153952"

print("Loading model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)

code = "print('Hello'"

prompt = f"""
Debug this code:

{code}
"""

inputs = tokenizer(prompt, return_tensors="pt")

outputs = model.generate(
    **inputs,
    max_length=128
)

result = tokenizer.decode(
    outputs[0],
    skip_special_tokens=True
)

print("\nPrediction:")
print(result)