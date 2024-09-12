import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine

# Parameters for the soundtrack
duration = 5000  # 5 seconds in milliseconds
frequency = 440  # Frequency of the sound in Hertz (A4 note)

# Generate a sine wave
sine_wave = Sine(frequency).to_audio_segment(duration=duration)

# Optionally, add another sine wave with a different frequency for a richer sound
overlay_wave = Sine(523).to_audio_segment(duration=duration)  # C5 note
sine_wave = sine_wave.overlay(overlay_wave)

# Export the generated audio as an MP3 file
sine_wave.export("amazing_soundtrack.mp3", format="mp3")

print("Soundtrack saved as 'amazing_soundtrack.mp3'")
