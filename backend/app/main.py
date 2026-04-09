
from fastapi import FastAPI
from api.scan import router as scan_router

app = FastAPI(title="SentinelScan API")

app.include_router(scan_router)

@app.get("/")
def home():
    return {"message": "SentinelScan backend running"}
