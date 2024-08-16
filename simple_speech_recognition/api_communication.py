import requests
from api_secrets import API_KEY_ASSEMBLYAI, API_KEY_LISTENNOTES
import time
import json

# Upload file to Assembly AI
upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'

# Authentication API key
assemblyai_headers = {'authorization': API_KEY_ASSEMBLYAI}

# Parameters
CHUNK_SIZE = 5_242_880 # 5MB

# Upload file, return audio_url
def upload(filename):
    def read_file(filename):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint,
                            headers=assemblyai_headers,
                            data=read_file(filename))

    audio_url = upload_response.json()['upload_url']
    return audio_url

# Transcribe
def transcribe(audio_url, sentiment_analysis):
    transcript_request = {
        "audio_url": audio_url,
        "sentiment_analysis": sentiment_analysis,
        }
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=assemblyai_headers)
    job_id = transcript_response.json()['id']
    return job_id

# Status Poll till done
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + "/" + transcript_id
    polling_response = requests.get(polling_endpoint, headers=assemblyai_headers)
    return polling_response.json()

def get_transcription_result_url(audio_url, sentiment_analysis):
    transcript_id = transcribe(audio_url, sentiment_analysis)
    while True:
        result = poll(transcript_id)
        if result['status'] == 'completed':
            return result, None
        elif result['status'] == 'error':
            return result, result['error']
        print('Waiting 60 seconds....')
        time.sleep(60)


# Save transcript into a txt file
def save_transcript(audio_url,filename, sentiment_analysis=False):
    result, error = get_transcription_result_url(audio_url, sentiment_analysis)

    if result:
        output_file = filename + '.txt'
        with open(output_file, 'w') as f:
            f.write(result['text'])
        if sentiment_analysis:
            output_file = filename + "_sentiment.json"
            with open(output_file, "w") as f:
                sentiments = result['sentiment_analysis_results']
                json.dump(sentiments, f, indent=4 )
        print('Transcription saved!!!')
    elif error:
        print('Error!!', error)