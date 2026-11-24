"""
Unit tests for PodX Professional Audio Mastering Pipeline.
"""
import numpy as np
import pytest
from audio_engine.mastering.masterer import AudioMasterer

def test_high_pass_filter():
    sr = 24000
    # Generate 40 Hz rumble + 1000 Hz tone
    t = np.linspace(0, 1.0, sr, endpoint=False)
    rumble = np.sin(2 * np.pi * 30 * t)  # 30 Hz sub-rumble
    tone = np.sin(2 * np.pi * 1000 * t)  # 1 kHz dialogue frequency
    signal = rumble + tone

    filtered = AudioMasterer.apply_high_pass_filter(signal, sr, cutoff_hz=80.0)
    
    # Energy at 30 Hz should be substantially attenuated
    fft_orig = np.abs(np.fft.rfft(signal))
    fft_filt = np.abs(np.fft.rfft(filtered))
    freqs = np.fft.rfftfreq(len(signal), 1.0 / sr)

    rumble_bin = np.argmin(np.abs(freqs - 30.0))
    assert fft_filt[rumble_bin] < (fft_orig[rumble_bin] * 0.15)

def test_true_peak_limiting_and_lufs():
    sr = 24000
    t = np.linspace(0, 3.0, 3 * sr, endpoint=False)
    # Generate loud speech-like synthetic tone
    signal = 0.9 * np.sin(2 * np.pi * 440 * t)

    mastered, lufs, peak = AudioMasterer.master_audio(
        signal, sr, target_lufs=-16.0, true_peak_limit=-1.0
    )

    # True peak must be <= -1.0 dBTP (+ margin)
    assert peak <= -0.95
    # Loudness must be normalized close to -16 LUFS
    assert abs(lufs - (-16.0)) <= 3.0
