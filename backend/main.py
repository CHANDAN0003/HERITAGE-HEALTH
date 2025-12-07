from fastapi import FastAPI, WebSocket
import asyncio
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import time
import numpy as np

from .model import predict
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

        ax = np.array(data["ax"])

        features = [
            float(np.mean(ax)),
            float(np.std(ax)),
            float(np.max(ax)),
            float(np.min(ax))
        ]

        y, score = predict(features)

        twin.update_pillar("P1", score)
        twin.update_pillar("P2", score / 2)
        twin.update_pillar("P3", score / 3)
        twin.update_pillar("P4", score / 4)

        twin.update_building_health()

        await websocket.send_json(twin.get_state())
        await asyncio.sleep(2)
