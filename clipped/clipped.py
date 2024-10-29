import numpy as np
import wave
import sounddevice as sd
import time
import argparse

parser = argparse.ArgumentParser( 
    description="Generate and play sine wave audio. And then do it again but clipped and different sounding.")
parser.add_argument('-p', '--pause', action='store_true', help="Add a 1/2 second  pause between playbacks.")
parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
args = parser.parse_args()

sample_rate = 44100       # samples per second
duration    = 1.0         # duration in seconds
frequency   = 440.0       # frequency of the sine wave (in Hz)
amplitude   = 32767       # max amplitude for 16-bit audio

# Generate the sine wave
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
sin_waveform = amplitude * 0.25 * np.sin(2 * np.pi * frequency * t)
sin_waveform = sin_waveform.astype(np.int16)

# Write the original sine wave to 'sin.wav'
if args.verbose:
    print("Writing sin.wav...")
with wave.open('sin.wav', 'w') as wav_file:
    wav_file.setnchannels(1) # mono audio
    wav_file.setsampwidth(2) # 16-bit audio
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(sin_waveform.tobytes())

# Clipping the waveform: limit values to ±8192
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
clipped_waveform = amplitude * 0.5 * np.sin(2 * np.pi * frequency * t)
clipped_waveform = clipped_waveform.astype(np.int16)
clip_limit = 8192
clipped_waveform = np.clip(clipped_waveform, -clip_limit, clip_limit)

# Write the clipped waveform to 'clipped.wav'
if args.verbose:
    print("Writing clipped.wav...")
with wave.open('clipped.wav', 'w') as wav_file:
    wav_file.setnchannels(1)           # mono audio
    wav_file.setsampwidth(2)           # 16-bit audio
    wav_file.setframerate(sample_rate) # sample rate
    wav_file.writeframes(clipped_waveform.tobytes())

# Play the original sine wave
if args.verbose:
    print("Playing generated sound...")
sd.play(sin_waveform, sample_rate)
sd.wait()

# Pause
if args.pause:
    if args.verbose:
        print("Pausing...")
    time.sleep(0.5)

# Play the clipped sine wave
if args.verbose:
    print("Playing clipped sound...")
sd.play(clipped_waveform, sample_rate)
sd.wait()

print("Thank you for running this program.")
