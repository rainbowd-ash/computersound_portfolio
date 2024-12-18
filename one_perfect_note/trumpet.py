import numpy as np
import sounddevice as sd
import scipy.signal as signal
import argparse

note_frequencies = {
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23,
    "G4": 392.00, "A4": 440.00, "B4": 493.88
}

def generate_trumpet_wave(frequency, duration=1.0, sampling_rate=44100):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

    base_wave = 0.6 * np.sin(2 * np.pi * frequency * t)
    second_harmonic = 0.3 * np.sin(2 * np.pi * 2 * frequency * t)
    third_harmonic = 0.2 * np.sin(2 * np.pi * 3 * frequency * t)
    trumpet_wave = base_wave + second_harmonic + third_harmonic

    attack_time = 0.05
    decay_time = 0.1
    sustain_level = 0.8
    release_time = 0.1

    envelope = np.ones_like(t)
    attack_samples = int(sampling_rate * attack_time)
    decay_samples = int(sampling_rate * decay_time)
    release_samples = int(sampling_rate * release_time)
    sustain_samples = len(t) - attack_samples - decay_samples - release_samples

    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    envelope[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain_level, decay_samples)
    envelope[attack_samples + decay_samples:attack_samples + decay_samples + sustain_samples] = sustain_level
    envelope[-release_samples:] = np.linspace(sustain_level, 0, release_samples)

    trumpet_wave *= envelope
    return trumpet_wave

parser = argparse.ArgumentParser(description="Play a trumpetish sound for a specified note.")
parser.add_argument("-n", "--note", type=str, default="A4", help="Note to play (e.g., C4, D4, A4) or frequency in Hz. Default is A4.")
parser.add_argument("-d", "--duration", type=float, default=1.0, help="Duration of the note in seconds. Default is 1 second.")

args = parser.parse_args()

if args.note in note_frequencies:
    frequency = note_frequencies[args.note]
else:
    try:
        frequency = float(args.note)
    except ValueError:
        print("Invalid note or frequency. Please enter a note (eg: A4) or a frequency in Hz.")
        exit(1)

trumpet_wave = generate_trumpet_wave(frequency, duration=args.duration)
sd.play(trumpet_wave, samplerate=44100)
sd.wait()
