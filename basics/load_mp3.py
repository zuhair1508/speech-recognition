# Download https://sourceforge.net/projects/ffmpeg-windows-builds, place files in bin folder and place path to env, 
# Install pydub
# Install build tools for Visual Studio 2022
from pydub import AudioSegment

# Read audio file
audio = AudioSegment.from_wav("sample.wav")

# Increase the volume by 6dB
audio = audio + 6

# Repeat
audio = audio * 2

# Fade in 
audio = audio.fade_in(2000)

# Save
audio.export("mashup.mp3", format="mp3")

audio2 = AudioSegment.from_mp3("mashup.mp3")
print("Done")