from fastapi import FastAPI, BackgroundTasks
from pipeline import run_pipeline

app = FastAPI()

@app.get("/")
def home():
    return {"message": "SentinelScan Backend Running"}

@app.post("/process")
async def process_issue(data: dict, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_pipeline, data)
    return {"status": "accepted"}
