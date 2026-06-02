import json

dataset = []

# Missing Parenthesis
for i in range(20):
    dataset.append({
        "buggy_code": f'print("Hello {i}"',
        "fixed_code": f'print("Hello {i}")',
        "explanation": "Missing closing parenthesis."
    })

# Missing Colon in if
for i in range(20):
    dataset.append({
        "buggy_code": f'if x == {i}\n    print(x)',
        "fixed_code": f'if x == {i}:\n    print(x)',
        "explanation": "Missing colon in if statement."
    })

# Missing Colon in for
for i in range(20):
    dataset.append({
        "buggy_code": f'for i in range({i+1})\n    print(i)',
        "fixed_code": f'for i in range({i+1}):\n    print(i)',
        "explanation": "Missing colon in for loop."
    })

# Division By Zero
for i in range(20):
    dataset.append({
        "buggy_code": f'result = {i+10} / 0',
        "fixed_code": f'result = {i+10} / 1',
        "explanation": "Division by zero causes runtime errors."
    })

# Name Error
for i in range(20):
    dataset.append({
        "buggy_code": f'print(user_name_{i})',
        "fixed_code": f'user_name_{i} = "John"\nprint(user_name_{i})',
        "explanation": "Variable used before definition."
    })

# Type Error
for i in range(20):
    dataset.append({
        "buggy_code": f'"{i}" + {i}',
        "fixed_code": f'str({i}) + "{i}"',
        "explanation": "Cannot concatenate string and integer directly."
    })

with open("../datasets/debug_dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)

print(f"Dataset generated successfully!")
print(f"Total examples: {len(dataset)}")