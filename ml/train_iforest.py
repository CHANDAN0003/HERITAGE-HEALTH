import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os
from processing.fft import extract_features

# Generate synthetic normal data for training
# We'll simulate vibration signals as mixtures of sinusoids + noise

def synth_signal(fs=200, n=500, freqs=[5,12], amps=[0.1,0.05], noise=0.01):
    t = np.arange(n) / fs
    s = np.zeros(n)
    for f,a in zip(freqs, amps):
        s += a * np.sin(2*np.pi*f*t)
    s += np.random.normal(0, noise, size=n)
    return s


def make_feature_matrix(n_samples=500, fs=200):
    rows = []
    for _ in range(n_samples):
        # vary frequencies slightly and amplitudes
        base_freqs = [5 + np.random.randn()*0.2, 12 + np.random.randn()*0.5]
        amps = [0.08 + np.random.rand()*0.04, 0.04 + np.random.rand()*0.03]
        s = synth_signal(fs=fs, n=500, freqs=base_freqs, amps=amps, noise=0.01 + np.random.rand()*0.02)
        feat = extract_features(s, fs=fs)
        rows.append([feat[k] for k in ["peak_freq","peak_amp","spectral_energy","harmonic_count","vib_var","tilt_rate"]])
    return np.array(rows)


def train_and_save(path="models/iforest.joblib"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    X = make_feature_matrix(n_samples=800, fs=200)
    clf = IsolationForest(n_estimators=200, contamination=0.01, random_state=42)
    clf.fit(X)
    joblib.dump(clf, path)
    print("Saved model to", path)

if __name__ == '__main__':
    train_and_save()
