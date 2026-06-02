from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

from db import debug_history

app = FastAPI(
    title="AI Debugging Assistant",
    description="Code Debugging API",
    version="1.0.0"
)

# ==================================
# CORS
# ==================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================================
# Request Model
# ==================================

class CodeRequest(BaseModel):
    code: str

# ==================================
# Home Route
# ==================================

@app.get("/")
def home():
    return {
        "message": "AI Debugging Assistant Running"
    }

# ==================================
# Debug Route
# ==================================

@app.post("/debug")
def debug_code(request: CodeRequest):

    code = request.code.strip()

    bug = "No obvious issue detected"
    fixed_code = code
    explanation = "The debugger could not identify a known issue."

    # Missing closing parenthesis
    if "print(" in code and not code.endswith(")"):
        bug = "Missing closing parenthesis"
        fixed_code = code + ")"
        explanation = (
            "The print statement requires a closing parenthesis."
        )

    # Missing colon in if statement
    elif "if " in code and ":" not in code:
        bug = "Missing colon"
        fixed_code = code + ":"
        explanation = (
            "Python if statements require a colon at the end."
        )

    # Missing colon in for loop
    elif "for " in code and ":" not in code:
        bug = "Missing colon"
        fixed_code = code + ":"
        explanation = (
            "Python for loops require a colon at the end."
        )

    # Division by zero
    elif "/ 0" in code or "/0" in code:
        bug = "Division by zero"
        fixed_code = code.replace("/0", "/1").replace("/ 0", "/ 1")
        explanation = (
            "Division by zero causes a runtime error."
        )

    # Name error
    elif "print(user_name)" in code:
        bug = "Undefined variable"
        fixed_code = (
            'user_name = "John"\n'
            'print(user_name)'
        )
        explanation = (
            "Variable used before it was defined."
        )

    # Type error
    elif '"5" + 5' in code or "'5' + 5" in code:
        bug = "Type mismatch"
        fixed_code = 'str(5) + "5"'
        explanation = (
            "Cannot concatenate a string and an integer directly."
        )

    # Store in MongoDB
    debug_history.insert_one({
        "buggy_code": code,
        "bug": bug,
        "fixed_code": fixed_code,
        "explanation": explanation,
        "created_at": datetime.utcnow()
    })

    return {
        "status": "success",
        "bug": bug,
        "fixed_code": fixed_code,
        "explanation": explanation
    }