import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("ANTHROPIC_API_KEY")

print("--- ENV DEBUGGER ---")
print(f"Current Working Directory: {os.getcwd()}")
print(f"Key found: {key if key else '❌ NOT FOUND (None)'}")
if key:
    print(f"Key starts with: {key[:10]}...")