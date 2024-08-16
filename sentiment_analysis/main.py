import sys
import json
from yt_extractor import get_audio_url, get_video_info
from api_secrets import API_KEY_ASSEMBLYAI
from api_communication import save_transcript

# Input video url
# video_url = sys.argv[1]

# Input sentiment file
# sentiment_file = "C:\Users\Amirah\Python_Projects\speech-recognition\sentiment_analysis\data\Apple_iPhone_13_review_sentiment.json"
sentiment_file = sys.argv[1]

def save_video_sentiments(url):
    video_infos = get_video_info(url)
    audio_url = get_audio_url(video_infos)
    title = video_infos['title']
    title = title.strip().replace(" ","_")
    title = "data/" + title
    save_transcript(audio_url, title, sentiment_analysis=True)

def analyze_sentiments(sentiment_file):
    with open(sentiment_file, 'r') as f:
        data = json.load(f)

    positives = []
    negatives = []
    neutrals = []

    for result in data:
        text = result['text']
        if result['sentiment'] == "POSITIVE":
            positives.append(text)
        elif result['sentiment'] == "NEGATIVE":
            negatives.append(text)
        else:
            neutrals.append(text)

    n_pos = len(positives)
    n_neg = len(negatives)
    n_neut = len(neutrals)

    print("Number of positives: ", n_pos)
    print("Number of negatives: ", n_neg)
    print("Number of neutrals: ", n_neut)

    # Calc ratio, ignore neutrals
    r = n_pos / (n_pos + n_neg)
    print(f"Positive ratio: {r:.3f}")

if __name__ == "__main__":
    # save_video_sentiments(video_url)
    analyze_sentiments(sentiment_file)
    
    