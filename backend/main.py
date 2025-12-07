from fastapi import FastAPI, WebSocket
import asyncio
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import time
import numpy as np

from ml.predict import score_payload
from .digital_twin import BuildingTwin

app = FastAPI()
twin = BuildingTwin()

# Mount frontend static files under /static to avoid catching WebSocket scopes
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve index.html at root (HTTP GET only)
@app.get("/")
async def root():
    return FileResponse("frontend/index.html")
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        with open("data/live.json") as f:
            data = json.load(f)

        # Use the new ML predictor which returns health_score and details
        result = score_payload(data, fs=200)
        if "error" in result:
            model_score = 0.0
            health = 100
        else:
            model_score = float(result.get("score", 0.0))
            health = int(result.get("health_score", 100))

        # Convert health to a normalized anomaly metric (0..1)
        anomaly_metric = (100 - health) / 100.0

        twin.update_pillar("P1", anomaly_metric)
        twin.update_pillar("P2", anomaly_metric / 2)
        twin.update_pillar("P3", anomaly_metric / 3)
        twin.update_pillar("P4", anomaly_metric / 4)

        twin.update_building_health()

        payload = twin.get_state()
        payload["model"] = result
        await websocket.send_json(payload)
        await asyncio.sleep(2)
