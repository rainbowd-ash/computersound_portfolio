import sounddevice as sd
import time
import sine_wave_generator as swg

sample_rate   = 44100
frequency     = 440.0 # Base frequency of the sine wave (in Hz)
amplitude     = 32767 # Max amplitude for 16-bit audio
beat_duration = 0.50  # 120 BPM

# Generate each wave segment
clipped_waveform = swg.generate_clipped_wave(frequency, amplitude, beat_duration)
volume_mod_waveform = swg.generate_volume_modulated_wave(frequency, amplitude, beat_duration)
high_freq_waveform = swg.generate_high_pitch_wave(frequency, amplitude, beat_duration)

def fade_out(waveform, duration, sample_rate=44100):
    """Applies a fade-out effect to the given waveform."""
    fade_length = int(sample_rate * duration)
    fade = np.linspace(1, 0, fade_length)
    waveform[-fade_length:] *= fade
    return waveform

# Define the rhythm pattern for each measure (4 beats)
def play_measure():
    # Beat 1
    sd.play(clipped_waveform, sample_rate)
    sd.wait()

    # Beat 2
    sd.play(volume_mod_waveform, sample_rate)
    sd.wait()

    # Beat 3
    time.sleep(beat_duration)

    # Beat 4
    sd.play(high_freq_waveform, sample_rate)
    sd.wait()

# Play the rhythm pattern a few times
print("My beatiful song...\n")
for _ in range(4):  # Play 4 measures
    play_measure()
print("Thank you for listening.")
