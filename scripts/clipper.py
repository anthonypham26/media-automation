import os
from pytubefix import YouTube


def download_video(url):
    yt = YouTube(url)
    yt.streams.filter(res = "1080p").first().download('videos/')
    print(f'Title: {yt.title}')

download_video('https://youtu.be/PugKQZHPut8?si=V2EtRZqJ9yFkf3BU')









# def crop_vertical():

#     return 0

# import whisper
# def generate_subtitles(audio_file):
#     model = whisper.load_model("base.en")

#     return 0

# def split_video_into_minute():

#     return 0

# def run_clipper():

#     return 0
