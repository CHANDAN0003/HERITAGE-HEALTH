import numpy as np
from sklearn.ensemble import IsolationForest

model = IsolationForest(contamination=0.1)

# Train on normal random data
X_train = np.random.normal(0, 1, (300, 4))
model.fit(X_train)

def predict(features):
    score = model.decision_function([features])[0]
    y = model.predict([features])[0]
    return y, score
