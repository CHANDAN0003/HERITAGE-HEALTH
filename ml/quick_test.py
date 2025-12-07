from ml.predict import load_model, score_payload
import numpy as np

print('Loading model...')
load_model()
print('Model loaded')
payload={'ax': (np.random.normal(0,0.02,500)).tolist(), 'tilt':0.01}
res=score_payload(payload, fs=200)
print('Score payload:', res)
