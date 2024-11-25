import argparse
import numpy as np
import wave

# get wav, return sample rate and file
def load_wave(filename):
    with wave.open(filename, 'r') as wav_file:
        sample_rate = wav_file.getframerate()
        n_channels = wav_file.getnchannels()
        n_frames = wav_file.getnframes()
        wave_data = np.frombuffer(wav_file.readframes(n_frames), dtype=np.int16)
        wave_data = wave_data.reshape(-1, n_channels).astype(np.float32) / 32768  # Normalize to -1 to 1
        return sample_rate, wave_data

# save wav
def save_wave(filename, data, sample_rate):
    n_channels = data.shape[1] if len(data.shape) > 1 else 1
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(n_channels)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_data = (data * 32767).astype(np.int16)
        wav_file.writeframes(wav_data.tobytes())

# apply wah
    # wave_data: waveform data as numpy array
    # sample_rate: sample rate of the waveform
    # wah_freq: frequency of the wah effect in hz
    # wet_dry: mix of the effect: 0 = dry, 1 = wet
def apply_wah_effect(wave_data, sample_rate, wah_freq, wet_dry):
    duration = len(wave_data) / sample_rate
    t = np.linspace(0, duration, len(wave_data), endpoint=False)
    wah = 0.5 + 0.5 * np.sin(2 * np.pi * wah_freq * t)  # Amplitude modulation

    if wave_data.ndim == 1:  # Mono
        wah_effect = wave_data * wah
        return (1 - wet_dry) * wave_data + wet_dry * wah_effect
    elif wave_data.ndim == 2:  # Stereo
        wah_effect = np.zeros_like(wave_data)
        for channel in range(wave_data.shape[1]):
            wah_effect[:, channel] = wave_data[:, channel] * wah
        return (1 - wet_dry) * wave_data + wet_dry * wah_effect
    else:
        raise ValueError("Too many (or too few!) channels in wav data")

def main():
    parser = argparse.ArgumentParser(description="Apply a wah effect to a WAV file.")
    parser.add_argument("-i", "--input", required=True, help="Input WAV file")
    parser.add_argument("-o", "--output", required=True,  help="Output WAV file")
    parser.add_argument("-f", "--freqency", type=float, default=1.0, help="Wah effect frequency (Hz)")
    parser.add_argument("-w", "--wet-dry", type=float, default=0.5, help="Wet/dry mix (0.0 = dry, 1.0 = wet)")

    args = parser.parse_args()

    # Load input WAV
    sample_rate, wave_data = load_wave(args.input)

    # Apply the wah effect
    wah_wave = apply_wah_effect(wave_data, sample_rate, args.freqency, args.wet_dry)

    # Save the output WAV
    save_wave(args.output, wah_wave, sample_rate)

if __name__ == "__main__":
    main()
