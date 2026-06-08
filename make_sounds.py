import wave
import struct
import math
import random

def generate_tone(filename, freq, duration, volume=0.8, sound_type="jump"):
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    with wave.open(filename, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        for i in range(num_samples):
            if sound_type == "jump":
                # Pitch sweep up
                current_freq = freq + (i / num_samples) * 400
                value = int(volume * 32767.0 * math.sin(2.0 * math.pi * current_freq * (i / sample_rate)))
            else:
                # Noise / explosion
                value = int(volume * 32767.0 * random.uniform(-1, 1) * math.exp(-i/(sample_rate*0.1)))
            data = struct.pack('<h', value)
            w.writeframesraw(data)

generate_tone('jump.wav', 300, 0.2, 0.9, "jump")
generate_tone('crash.wav', 100, 0.4, 0.9, "crash")
