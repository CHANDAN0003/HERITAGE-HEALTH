import numpy as np
from scipy.signal import find_peaks

def compute_fft(signal, fs):
    """Compute single-sided FFT and return frequencies and magnitudes."""
    n = len(signal)
    # apply window to reduce spectral leakage
    window = np.hanning(n)
    sig = signal * window
    fft = np.fft.rfft(sig)
    mags = np.abs(fft) / (n/2)
    freqs = np.fft.rfftfreq(n, d=1.0/fs)
    return freqs, mags


def extract_features(ax, ay=None, az=None, tilt=None, fs=200):
    """Extract features from acceleration arrays and optional tilt.

    Parameters
    - ax, ay, az: 1D numpy arrays of acceleration (time domain)
    - tilt: float or time series (if time series, can compute stats)
    - fs: sampling frequency

    Returns: dict of features
    """
    # prefer using resultant magnitude if multiple axes provided
    if ay is not None and az is not None:
        mag = np.sqrt(np.array(ax)**2 + np.array(ay)**2 + np.array(az)**2)
    else:
        mag = np.array(ax)

    mag = mag.astype(float)

    # basic time-domain stats
    vib_mean = float(np.mean(mag))
    vib_std = float(np.std(mag))
    vib_var = float(np.var(mag))
    vib_max = float(np.max(mag))
    vib_min = float(np.min(mag))

    # FFT
    freqs, mags = compute_fft(mag, fs)

    # find peaks in magnitude spectrum
    peaks, properties = find_peaks(mags, height=np.max(mags)*0.05)
    peak_freqs = freqs[peaks]
    peak_amps = mags[peaks]

    # sort peaks by amplitude desc
    if len(peak_amps) > 0:
        order = np.argsort(peak_amps)[::-1]
        peak_freqs = peak_freqs[order]
        peak_amps = peak_amps[order]
    else:
        peak_freqs = np.array([])
        peak_amps = np.array([])

    peak_res_freq = float(peak_freqs[0]) if peak_freqs.size>0 else 0.0
    peak_res_amp = float(peak_amps[0]) if peak_amps.size>0 else 0.0

    spectral_energy = float(np.sum(mags**2))

    # harmonic count: count peaks that are integer multiples of the fundamental
    harmonic_count = 0
    if peak_freqs.size > 1 and peak_res_freq > 0:
        ratios = peak_freqs / peak_res_freq
        # consider harmonic if within 5% of integer
        harmonic_count = int(np.sum(np.isclose(ratios, np.round(ratios), atol=0.05)))

    # tilt features
    tilt_dev = None
    tilt_rate = None
    if tilt is None:
        tilt_dev = 0.0
        tilt_rate = 0.0
    else:
        try:
            # if tilt is a time series
            t = np.array(tilt)
            tilt_dev = float(np.std(t))
            # approximate rate per second
            if t.size >= 2:
                tilt_rate = float((t[-1] - t[0]) / (len(t)/fs))
            else:
                tilt_rate = 0.0
        except Exception:
            # tilt is a single float
            tilt_dev = 0.0
            tilt_rate = float(tilt)

    features = {
        "vib_mean": vib_mean,
        "vib_std": vib_std,
        "vib_var": vib_var,
        "vib_max": vib_max,
        "vib_min": vib_min,
        "peak_freq": peak_res_freq,
        "peak_amp": peak_res_amp,
        "spectral_energy": spectral_energy,
        "harmonic_count": harmonic_count,
        "tilt_dev": tilt_dev,
        "tilt_rate": tilt_rate,
    }

    return features
