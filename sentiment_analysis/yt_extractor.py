import yt_dlp

ydl = yt_dlp.YoutubeDL()

def get_video_info(url):
    with ydl:
        result = ydl.extract_info(
            url,
            download=False
        )

    if "entries" in result:
        return result['entries'][0]
    return result

def get_audio_url(video_info):
    for x in video_info['formats']:
        if x['ext'] == 'm4a':#$ x['url'])
            return x['url']


if __name__ == "__main__":
    video_info = get_video_info("https://www.youtube.com/watch?v=rz_rus8Vg6Q")
    audio_url = get_audio_url(video_info)
    print(audio_url)