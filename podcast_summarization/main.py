# podcasts from https://www.listennotes.com/api/
from api_communication import *
import streamlit as st
import json

st.title('Podcast Summaries')
episode_id = st.sidebar.text_input('Please input an episode id')
sentiment_analysis=False
auto_chapters=True
button = st.sidebar.button("Get podcast summary!", on_click=save_transcript, args=(episode_id, sentiment_analysis, auto_chapters))


def get_clean_time(start_ms):
    seconds = int((start_ms/1000) % 60)
    minutes = int((start_ms/(1000 * 60)) % 60)
    hours = int((start_ms/(1000 * 60 * 60)) % 24)

    if hours > 0:
        start_t = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        start_t = f'{minutes:02d}:{seconds:02d}'
    return start_t

if button:
    filename = episode_id + '_chapters.json'
    with open(filename, 'r') as f:
        data = json.load(f)

        chapters = data['chapters']
        podcast_title = data['podcast_title']
        episode_title = data['episode_title']
        thumbnail = data['episode_thumbnail']

    st.header(f'{podcast_title} - {episode_title}')
    st.image(thumbnail)

    for chp in chapters:
        with st.expander(chp['gist'] + ' - ' + get_clean_time(chp['start'])):
            chp['summary']
