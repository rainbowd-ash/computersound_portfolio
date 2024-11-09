import numpy as np
import argparse
import wave

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


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Generate a mosquito noise sine wave.")
    parser.add_argument("-f", "--frequency", type=float, default=900, help="Frequency of the sine wave in Hz")
    parser.add_argument("-a", "--amplitude", type=int, default=32767, help="Amplitude of the sine wave")
    parser.add_argument("-d", "--duration", type=float, default=2.0, help="Duration of the sine wave in seconds")
    parser.add_argument("-s", "--sample_rate", type=int, default=44100, help="Sample rate in Hz")
    parser.add_argument("-o", "--output", type=str, default="sine.wav", help="Output filename")

    args = parser.parse_args()

    # Generate the wave
    waveform = generate_sine_wave(args.frequency, args.amplitude, args.duration, args.sample_rate)

    # Save to a .wav file
    with wave.open(args.output, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono sound
        wav_file.setsampwidth(2)  # 16 bits per sample
        wav_file.setframerate(args.sample_rate)
        wav_file.writeframes(waveform.tobytes())
    print(f"Saved sine wave to {args.output}!")

if __name__ == "__main__":
    main()

