import os
from pytubefix import YouTube

#input: youtube url, outputs into videos/ and audios/
def download_video(url):
    yt = YouTube(url)
    video_file = yt.streams.filter(only_video= True, file_extension = 'mp4').order_by('resolution').desc().first()
    audio_file = yt.streams.filter(only_audio=True).first()
    video_file.download('videos/')
    audio_file.download(output_path= 'audios/', mp3 = True)
    print(f'Title: {yt.title}')

download_video('https://youtu.be/PugKQZHPut8?si=V2EtRZqJ9yFkf3BU')


def crop_vertical():

    return 0

def generate_subtitles(audio_file):
    # model = whisper.load_model("base.en")

    return 0

def split_video_into_minute():

    return 0

def run_clipper():

    return 0
