import wave
import matplotlib.pyplot as plt
import numpy as np

obj = wave.open("sample.wav", "rb")

sample_frequency = obj.getframerate()
n_samples = obj.getnframes()
signal_wave = obj.readframes(-1)

obj.close()

t_audio = n_samples / sample_frequency
print(f"Audio duration: {t_audio} seconds")

signal_array = np.frombuffer(signal_wave, dtype=np.int16)
time = np.linspace(start=0, stop=t_audio, num=n_samples)

plt.figure(figsize=(15,5))
plt.plot(time, signal_array)
plt.title("Audio Signal")
plt.ylabel("Signal Wave")
plt.xlabel("Time (s)")
plt.xlim(0, t_audio)
plt.show()