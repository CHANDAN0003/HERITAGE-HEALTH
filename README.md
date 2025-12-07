# HeritageHealth — Structural Health Monitoring Prototype

This repository contains a prototype for HeritageHealth: a non-invasive, AI-driven structural health monitoring system for heritage temples. It demonstrates a full-stack workflow: sensor simulator → FFT-based feature extraction → IsolationForest anomaly detection → real-time digital twin (3D frontend) via WebSocket.

**Key features**
- Simulated low-cost MEMS sensor data generator (time-domain vibration + tilt)
- FFT-based feature extraction (`processing/fft.py`)
- IsolationForest model training and prediction (`ml/train_iforest.py`, `ml/predict.py`)
- FastAPI backend that serves a WebSocket endpoint and a simple digital twin (`backend/main.py`)
- Three.js frontend visualizing pillars and live health status (`frontend/index.html`)

---

## Repo layout (important files)
- `simulator/sensor_simulator.py` — simple process that writes `data/live.json` periodically (used for local testing).
- `processing/fft.py` — FFT + feature extraction implementation used by ML pipeline.
- `ml/train_iforest.py` — generate synthetic "normal" data, train IsolationForest, save `models/iforest.joblib`.
- `ml/predict.py` — load model and provide `score_payload(payload, fs)` for runtime scoring.
- `backend/main.py` — FastAPI app: serves `frontend/index.html` on `/` and WebSocket on `/ws`.
- `backend/digital_twin.py` — simple building twin state manager.
- `frontend/index.html` — 3D visualization + WebSocket client that updates pillar colors and shows health info.
- `requirements.txt` — Python dependencies (update with `pip install -r requirements.txt`).

---

## Quick start (Windows, cmd.exe)
These steps assume you are at the repository root `D:\HERITAGE-HEALTH`.

1. Activate the virtual environment (if present):

```bat
D:\HERITAGE-HEALTH> venv\Scripts\activate.bat
```

2. Install dependencies (only needed once or after changes to `requirements.txt`):

```bat
(venv) D:\HERITAGE-HEALTH> python -m pip install --upgrade pip
(venv) D:\HERITAGE-HEALTH> python -m pip install -r requirements.txt
(venv) D:\HERITAGE-HEALTH> python -m pip install "uvicorn[standard]" websockets scipy scikit-learn joblib
```

3. (Optional) Train the IsolationForest model (creates `models/iforest.joblib`):

```bat
(venv) D:\HERITAGE-HEALTH> python -m ml.train_iforest
```

4. Start the sensor simulator in a separate terminal to generate `data/live.json`:

```bat
(venv) D:\HERITAGE-HEALTH> python simulator\sensor_simulator.py
# You should see repeated prints like: "Data written to data/live.json"
```

5. Start the FastAPI backend (another terminal):

```bat
(venv) D:\HERITAGE-HEALTH> uvicorn backend.main:app --reload
```

6. Open the frontend in your browser:

```
http://127.0.0.1:8000/
```

The frontend page connects to the backend WebSocket at `ws://127.0.0.1:8000/ws` and will update pillar colors and a health panel.

---

## Notes & troubleshooting

- If you get `404 Not Found` when visiting `/`, ensure `uvicorn` is running and that the backend log shows the GET request. The backend serves `frontend/index.html` at `/`.
- If you see `Unsupported upgrade request` or `No supported WebSocket library detected`, install `uvicorn[standard]` or `websockets` in the venv and restart the server.
- If WebSocket connections return `404`, ensure the URL used by the client is `ws://127.0.0.1:8000/ws` (not `http://`).
- If the frontend shows no updates, confirm the simulator is running and `data/live.json` is being updated every 2 seconds.
- If you delete `models/iforest.joblib`, recreate it with `python -m ml.train_iforest`.
- To conserve disk space you can remove `venv/` then recreate later with `python -m venv venv` and reinstall dependencies.

---

## Extending the project

- Replace file-based ingestion (`data/live.json`) with an ingestion endpoint (HTTP POST or WebSocket) so ESP32 devices can push data directly.
- Replace the synthetic training data with real historical normal data and retrain the IsolationForest.
- Add a persistence layer (SQLite or time-series DB) for historical graphs and alerts. The frontend can use Chart.js to display history.
- Harden the model and API for production: authentication, rate limiting, Docker packaging and deployment automation.

---

## Useful commands
- Run quick ML test (loads model and scores a synthetic payload):
```bat
(venv) D:\HERITAGE-HEALTH> python -m ml.quick_test
```

- Remove simulator data file (clean):
```bat
del simulator\data\live.json
```

---

If you want, I can also:
- Add a `/ingest` HTTP endpoint to receive JSON sensor payloads directly from devices.
- Add a Dockerfile and a `docker-compose.yml` for local deployment.
- Add simple history charts to the frontend using Chart.js and a tiny API to read recent data points.

If you'd like me to implement any of those next steps, tell me which one and I'll scaffold it.
