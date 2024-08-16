import sys
from api_communication import *

# Input file path of input file
filename = sys.argv[1]

# Workflow
audio_url = upload(filename)
save_transcript(audio_url, filename)