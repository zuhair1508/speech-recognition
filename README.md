### Basic Python Audio Processing Basics
- Audio formats
- Audio signal parameters
- Wave module to load and save a wav file
- Plotting a wave signal
- Microphone recording
- Load mp3

### Speech Recognition using AssemblyAI
Transcribe an audio file aka speech-to-text using AssemblyAI's speech-to-text transcription API

### Sentiment Classification
Transcribe a video file and using AssemblyAI's speech-to-text transcription API

### Podcast Summarization + Web Interface
Transcribe a ListenNotes Podcast using listennotes API by providing the episode_id, and returning the breakdown of the podcast by chapters and summaries.

### Real time speech recognition
Used AssemblyAI's speech-to-text transcription API to transcribe from the microphone in real time. We use PyAudio library to stream the sound from the mic and python websocket's library to connect to AssemblyAI's streaming websocket endpoint. We use OpenAI GPT-4o-mini to communicate with the chatbot and do Q&A in real time.
https://www.assemblyai.com/blog/real-time-speech-recognition-with-python/