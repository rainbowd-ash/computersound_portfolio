import numpy as np

def generate_sine_wave(frequency, amplitude, duration, sample_rate=44100):
    """Generates a sine wave at a given frequency, amplitude, and duration."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    waveform = amplitude * np.sin(2 * np.pi * frequency * t)
    return waveform.astype(np.int16)

def generate_clipped_wave(frequency, amplitude, duration, clip_limit=8192, sample_rate=44100):
    """Generates a sine wave with clipping applied."""
    waveform = generate_sine_wave(frequency, amplitude, duration, sample_rate)
    return np.clip(waveform, -clip_limit, clip_limit)

def generate_volume_modulated_wave(frequency, amplitude, duration, sample_rate=44100):
    """Generates a sine wave with volume modulation applied."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    volume_sweep = 0.5 + 0.5 * np.sin(2 * np.pi * 0.5 * t)  # Sweeps from 50% to 100%
    waveform = amplitude * volume_sweep * np.sin(2 * np.pi * frequency * t)
    return waveform.astype(np.int16)

def generate_high_pitch_wave(frequency, amplitude, duration, sample_rate=44100):
    """Generates a high-pitched sine wave at 1.5x the base frequency."""
    return generate_sine_wave(frequency * 1.5, amplitude, duration, sample_rate)

