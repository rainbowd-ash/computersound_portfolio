import numpy as np
import argparse
from scipy.io import wavfile
from scipy.signal import butter, sosfilt


def fft_energy_bands(waveform, sample_rate):
	"""Calculates the energy in low, mid, and high frequency bands of the waveform."""
	# Perform fast fourier transform on the waveform
	spectrum = np.fft.fft(waveform)
	freqs = np.fft.fftfreq(len(spectrum), 1 / sample_rate)

	# frequency ranges in Hz
	low_band = (0, 300)
	mid_band = (300, 2000)
	high_band = (2000, sample_rate // 2)

	# Calculate energy in each band
	low_energy = np.sum(np.abs(spectrum[(freqs >= low_band[0]) & (freqs < low_band[1])])**2)
	mid_energy = np.sum(np.abs(spectrum[(freqs >= mid_band[0]) & (freqs < mid_band[1])])**2)
	high_energy = np.sum(np.abs(spectrum[(freqs >= high_band[0]) & (freqs < high_band[1])])**2)

	return low_energy, mid_energy, high_energy


def calculate_gains(low_energy, mid_energy, high_energy):
	"""Calculates the gain needed for each band to equalize their energies."""
	target_energy = (low_energy + mid_energy + high_energy) / 3
	low_gain = np.sqrt(target_energy / low_energy) if low_energy > 0 else 1
	mid_gain = np.sqrt(target_energy / mid_energy) if mid_energy > 0 else 1
	high_gain = np.sqrt(target_energy / high_energy) if high_energy > 0 else 1

	return low_gain, mid_gain, high_gain


def apply_tone_filter(waveform, sample_rate, low_gain, mid_gain, high_gain):
	"""Applies low, mid, and high tone filters with specified gains to equalize band energy."""

	# Create bandpass filters for each band
	sos_low = butter(4, 300, btype='low', fs=sample_rate, output='sos')
	sos_mid = butter(4, [300, 2000], btype='bandpass', fs=sample_rate, output='sos')
	sos_high = butter(4, 2000, btype='high', fs=sample_rate, output='sos')

	# Apply each filter and adjust gain
	low_band = low_gain * sosfilt(sos_low, waveform)
	mid_band = mid_gain * sosfilt(sos_mid, waveform)
	high_band = high_gain * sosfilt(sos_high, waveform)

	# Combine bands to get the equalized waveform
	equalized_waveform = low_band + mid_band + high_band
	return equalized_waveform.astype(np.int16)


def equalize_bands(waveform, sample_rate):
	"""Equalizes the energy in low, mid, and high frequency bands of a waveform."""
	# Step 1: Calculate energy in each band
	low_energy, mid_energy, high_energy = fft_energy_bands(waveform, sample_rate)

	# Step 2: Calculate the gain for each band
	low_gain, mid_gain, high_gain = calculate_gains(low_energy, mid_energy, high_energy)

	# Step 3: Apply tone filters with calculated gains
	equalized_waveform = apply_tone_filter(waveform, sample_rate, low_gain, mid_gain, high_gain)

	return equalized_waveform


def main():
	parser = argparse.ArgumentParser(description="Equalize the frequency bands of a WAV file.")
	parser.add_argument("wavfile", type=str, help="Path to the input WAV file")
	args = parser.parse_args()

	sample_rate, waveform = wavfile.read(args.wavfile)

	# If stereo, take just one channel
	if len(waveform.shape) > 1:
		waveform = waveform[:, 0]

	equalized_waveform = equalize_bands(waveform, sample_rate)

	import sounddevice as sd
	sd.play(equalized_waveform, sample_rate)
	sd.wait()

if __name__ == "__main__":
	main()