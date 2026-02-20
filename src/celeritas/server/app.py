import os
from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from celeritas.storage.db import fetch_all_results
from celeritas.models import CombinedResult
from celeritas.core.runner import run_all_tests

api = FastAPI(title="Celeritas API")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

api.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@api.get("/")
def read_root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@api.get("/api/results", response_model=list[CombinedResult])
def get_results():
    """Fetch all historical test results"""
    return fetch_all_results()

@api.post("/api/run")
def trigger_run(background_tasks: BackgroundTasks):
    """Trigger a new speedtest asynchronously"""
    background_tasks.add_task(run_all_tests)
    return {"status": "Test started in background."}
