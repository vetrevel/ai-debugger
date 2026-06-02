from db import debug_history

debug_history.insert_one({
    "buggy_code": "print('Hello'",
    "fixed_code": "print('Hello')",
    "explanation": "Missing closing parenthesis"
})

print("Inserted Successfully")