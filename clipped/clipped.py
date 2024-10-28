import numpy as np
import wave

# Parameters
sample_rate = 44100       # samples per second
duration = 2.0            # duration in seconds
frequency = 440.0         # frequency of the sine wave (in Hz)
amplitude = 32767 / 4     # amplitude (max value for 16-bit audio / 4)

# Generate the sine wave
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)  # time variable
waveform = amplitude * np.sin(2 * np.pi * frequency * t)                   # sine wave formula
waveform = waveform.astype(np.int16)                                       # 16-bit audio

# Write to WAV file
with wave.open('sin.wav', 'w') as wav_file:
    # WAV file parameters
    wav_file.setnchannels(1)           # mono audio
    wav_file.setsampwidth(2)           # 16-bit audio
    wav_file.setframerate(sample_rate) # sample rate
    
    # Write the waveform data
    wav_file.writeframes(waveform.tobytes())

print("Created sine.wav")

