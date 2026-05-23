import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# 1. Force Python to find the .env file relative to THIS script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")
load_dotenv(dotenv_path=env_path)

# 2. Extract the key
MASTER_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# 3. 🚨 HARDCODE FALLBACK CRUTCH (Use this if os.getenv is returning None)
if not MASTER_API_KEY or MASTER_API_KEY == "your_actual_api_key_here":
    # Paste your real 'sk-ant-...' key right here between the quotes
    MASTER_API_KEY = "your_actual_api_key_here"

print(f"👁️ Server Boot Check - API Key Loaded: {MASTER_API_KEY[:10] if MASTER_API_KEY else 'EMPTY'}...")

from TestCaseGeneration import generate_gherkin_tests
from GherkinToPlaywright import translate_gherkin_to_playwright

app = FastAPI(title="AI Agentic QE Pipeline")

class JiraWebhookPayload(BaseModel):
    issue_key: str
    summary: str
    description: str

def run_agent_pipeline(issue_key: str, summary: str, description: str):
    print(f"\n⚡ Starting Agent Pipeline for {issue_key}: {summary}")
    
    # Secure validation check inside the background worker
    if not MASTER_API_KEY:
        print("❌ CRITICAL ERROR: MASTER_API_KEY is completely empty inside the background thread!")
        return

    full_requirement = f"Title: {summary}\nDescription: {description}"
    feature_file_path = f"{issue_key}_validation.feature"
    spec_file_path = f"{issue_key}.spec.ts"
    
    # ---- AGENT 1: Handing the key directly ----
    print(f"🤖 [Agent 1] Analyzing requirements for {issue_key}...")
    gherkin_output = generate_gherkin_tests(full_requirement, api_key=MASTER_API_KEY)
    
    with open(feature_file_path, "w", encoding="utf-8") as f:
        f.write(gherkin_output)
    print(f"💾 Saved Gherkin to {feature_file_path}")
    
    # ---- AGENT 2: Handing the key directly ----
    print(f"🚀 [Agent 2] Generating Playwright script for {issue_key}...")
    playwright_code = translate_gherkin_to_playwright(feature_file_path, api_key=MASTER_API_KEY)
    
    with open(spec_file_path, "w", encoding="utf-8") as f:
        f.write(playwright_code)
    print(f"✨ Success! Automation suite completely generated: {spec_file_path}\n")

@app.post("/webhook/jira-story")
async def receive_jira_story(payload: JiraWebhookPayload, background_tasks: BackgroundTasks):
    if not payload.description or not payload.issue_key:
        raise HTTPException(status_code=400, detail="Missing critical issue data.")
        
    background_tasks.add_task(
        run_agent_pipeline, 
        payload.issue_key, 
        payload.summary, 
        payload.description
    )
    
    return {
        "status": "Accepted", 
        "message": f"Agent pipeline triggered in background for ticket {payload.issue_key}"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)