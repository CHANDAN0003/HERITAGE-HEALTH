import numpy as np
from scipy.fft import fft

def extract_features(signal):
    yf = np.abs(fft(signal))
    return [
        np.mean(yf),
        np.std(yf),
        np.max(yf),
        np.min(yf)
    ]
