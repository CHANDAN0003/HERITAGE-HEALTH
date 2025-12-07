import joblib
import numpy as np
import os
from processing.fft import extract_features

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "iforest.joblib")

_model = None

def load_model(path=None):
    global _model
    p = path or MODEL_PATH
    p = os.path.abspath(p)
    if not os.path.exists(p):
        raise FileNotFoundError(f"Model not found at {p}. Train it with ml/train_iforest.py")
    _model = joblib.load(p)
    return _model


def score_payload(payload, fs=200):
    """Accept sensor payload dict with keys ax, ay?, az?, tilt? and return score & health

    Returns dict: {score, health_score, status, details}
    """
    ax = payload.get('ax')
    ay = payload.get('ay')
    az = payload.get('az')
    tilt = payload.get('tilt')

    feats = extract_features(ax, ay, az, tilt, fs=fs)
    X = np.array([[feats[k] for k in ["peak_freq","peak_amp","spectral_energy","harmonic_count","vib_var","tilt_rate"]]])

    global _model
    if _model is None:
        try:
            load_model()
        except Exception as e:
            return {"error": str(e)}

    score = float(_model.decision_function(X)[0])
    # IsolationForest decision_function: higher is more normal; anomalies have negative scores
    anomaly = _model.predict(X)[0] == -1

    # Map to 0-100 health score
    health_score = int(np.clip((score - -0.2) / (0.2 - -0.2) * 100, 0, 100))

    status = "ok"
    details = "normal"
    if anomaly:
        status = "warning"
        details = "anomaly_detected"
    if health_score < 40:
        status = "critical"

    return {
        "score": score,
        "health_score": health_score,
        "status": status,
        "details": details,
        "features": feats
    }

if __name__ == '__main__':
    # quick test: train a local model if not present
    try:
        load_model()
        print('Model loaded')
    except Exception:
        print('Model missing. Run ml/train_iforest.py to create a model.')
