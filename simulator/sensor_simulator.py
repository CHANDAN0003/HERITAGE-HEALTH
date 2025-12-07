import numpy as np
import json
import time

while True:
    data = {
        "ax": np.random.normal(0, 0.02, 500).tolist(),
        "ay": np.random.normal(0, 0.02, 500).tolist(),
        "az": np.random.normal(0, 0.02, 500).tolist()
    }

    # Inject anomaly sometimes
    if np.random.rand() > 0.85:
        data["ax"] = (np.sin(np.linspace(0, 20, 500)) * 1.2).tolist()

    with open("data/live.json", "w") as f:
        json.dump(data, f)
    print("Data written to data/live.json")
    time.sleep(2)
