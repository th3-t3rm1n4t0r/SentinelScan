from fastapi import FastAPI, BackgroundTasks, status
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv
import os

# Load the .env from wherever it's hiding in your project tree
load_dotenv(find_dotenv())

app = FastAPI(title="SentinelScan_Backend")

class WebhookPayload(BaseModel):
    repository_owner: str
    repository_name: str
    issue_number: str
    task_description: str

async def process_remediation(payload: WebhookPayload):
    # This is where Phase 3 (Git Tree) and Phase 4 (Presidio) will live
    print(f"[WORKER] Starting analysis for {payload.repository_name}")
    # Verify your key is actually loading in the background task
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"[WORKER] API Key loaded: {'Yes' if api_key else 'No'}")

@app.post("/webhook", status_code=status.HTTP_202_ACCEPTED)
async def intake_webhook(payload: WebhookPayload, background_tasks: BackgroundTasks):
    print(f"[API] Received Issue #{payload.issue_number}")
    background_tasks.add_task(process_remediation, payload)
    return {"status": "accepted"}