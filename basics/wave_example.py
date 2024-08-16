# Audio file formats
# .mp3 - lossy compression format
# .flac - loss less compression format, can reconstruct original data
# .wav - uncompressed format, largest file, standard CD quality

import wave

""" Audio Signal Parameters
- number of channels: mono or stereo
- sample width: number of bytes used to represent each sample
- framerate/sample_rate: number of samples per second i.e. 44.1 kHz
- number of frames: 
- values of a frame: 
"""

# Open audio file
obj = wave.open("sample.wav", "rb")

# Extract parameters
nchannels = obj.getnchannels()
sampwidth = obj.getsampwidth()
framerate = obj.getframerate()
nframes = obj.getnframes()
params = obj.getparams()

print("Number of channels: ", nchannels)
print("Sample width: ", sampwidth,)
print("Frame rate: ", framerate)
print("Number of frames: ", nframes)
print("Parameters: ", params)

# Audio duration
t_audio = nframes / framerate
print("Audio duration: ", t_audio, " seconds")

frames = obj.readframes(-1)
print(type(frames), type(frames[0]))
print(len(frames))  # Sample width * number of frames

# Close audio file
obj.close()

# Create new audio file
obj_new = wave.open("sample_new.wav", "wb")
obj_new.setnchannels(1)
obj_new.setsampwidth(2)
obj_new.setframerate(48000)

obj_new.writeframes(frames)
obj_new.close()