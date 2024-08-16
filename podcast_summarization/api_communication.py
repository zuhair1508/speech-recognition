import requests
from api_secrets import API_KEY_ASSEMBLYAI, API_KEY_LISTENNOTES
import time
import json
import pprint

# Upload file to Assembly AI
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'
listennotes_episode_endpoint = 'https://listen-api.listennotes.com/api/v2/episodes'

# Authentication API key
assemblyai_headers = {'authorization': API_KEY_ASSEMBLYAI}
listennotes_headers = {'X-ListenAPI-Key': API_KEY_LISTENNOTES}

# Parameters
CHUNK_SIZE = 5_242_880 # 5MB

# Get Episode ID and podcasts audio file
def get_episode_audio_url(episode_id):
    url = listennotes_episode_endpoint + '/' + episode_id
    response = requests.request('GET', url, headers=listennotes_headers)
    data = response.json()
    # pprint.pprint(data)
    audio_url = data['audio']
    episode_thumbnail = data['thumbnail']
    podcast_title = data['podcast']['title']
    episode_title = data['title']

    return audio_url, episode_thumbnail, podcast_title, episode_title

# Transcribe
def transcribe(audio_url, sentiment_analysis, auto_chapters):
    transcript_request = {
        "audio_url": audio_url,
        "sentiment_analysis": sentiment_analysis,
        "auto_chapters": auto_chapters
        }
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=assemblyai_headers)
    job_id = transcript_response.json()['id']
    return job_id

# Status Poll till done
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + "/" + transcript_id
    polling_response = requests.get(polling_endpoint, headers=assemblyai_headers)
    return polling_response.json()

def get_transcription_result_url(audio_url, sentiment_analysis, auto_chapters):
    transcript_id = transcribe(audio_url, sentiment_analysis, auto_chapters)
    while True:
        result = poll(transcript_id)
        if result['status'] == 'completed':
            return result, None
        elif result['status'] == 'error':
            return result, result['error']
        print('Waiting 60 seconds....')
        time.sleep(60)


# Save transcript into a txt file
def save_transcript(episode_id, sentiment_analysis=False, auto_chapters=False):
    audio_url, episode_thumbnail, podcast_title, episode_title = get_episode_audio_url(episode_id)
    result, error = get_transcription_result_url(audio_url, sentiment_analysis, auto_chapters)

    # pprint.pprint(result)

    if result:
        if auto_chapters:
            output_file = episode_id + '.txt'
            with open(output_file, 'w') as f:
                f.write(result['text'])

            chapters_file = episode_id + '_chapters.json'
            with open(chapters_file, 'w') as f:
                chapters = result['chapters']
                episode_data = {'chapters': chapters}
                episode_data['episode_thumbnail'] = episode_thumbnail
                episode_data['podcast_title'] = podcast_title
                episode_data['episode_title'] = episode_title
                json.dump(episode_data, f)
                print("Transcript saved!!!")
                return True

        if sentiment_analysis:
            output_file = filename + "_sentiment.json"
            with open(output_file, "w") as f:
                sentiments = result['sentiment_analysis_results']
                json.dump(sentiments, f, indent=4 )
        print('Transcription saved!!!')
            
    elif error:
        print('Error!!', error)