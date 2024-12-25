import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment
from os import listdir

def generate_tone(frequency, duration, sample_rate=44100, amplitude=0.5):
    """
    Generate a single-tone sine wave.
    
    :param frequency: Frequency of the tone in Hz.
    :param duration: Duration of the tone in seconds.
    :param sample_rate: Sampling rate in Hz.
    :param amplitude: Amplitude of the wave (0.0 to 1.0).
    :return: NumPy array representing the tone.
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    tone = amplitude * np.sin(2 * np.pi * frequency * t)
    return np.int16(tone * 32767)  # Convert to 16-bit PCM format

def createFile(fileName:str) -> None:

    if not fileName in listdir():
        with open(fileName,"w"):
            pass
        print("file was created")

# Generate a tone
frequency = 700  # A4 note (440 Hz)
duration = 0.06 * 3 # 2 seconds
sample_rate = 44100  # Standard sample rate
amplitude = 0.5  # Medium loudness

tone = generate_tone(frequency, duration, sample_rate, amplitude)

# Save the tone as a WAV file
"""wav_filename = "morse_short.wav"
write(wav_filename, sample_rate, tone)"""

# Convert the WAV file to MP3 using Pydub
mp3_filename = "morse_long.mp3"
createFile(mp3_filename)
write(mp3_filename, sample_rate, tone)
audio = AudioSegment.from_mp3(mp3_filename)
audio.export(mp3_filename, format="mp3")

print(f"Tone saved as {mp3_filename}")
