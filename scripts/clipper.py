import os
from pytubefix import YouTube
import ffmpeg
import moviepy.editor as mpy
from moviepy.video.fx.all import crop

# input: youtube url, outputs into videos/ and audios/
def download_video(url):
    yt = YouTube(url)
    print(f"Downloading {yt.title} from Youtube")
    video_file = yt.streams.filter(only_video= True, file_extension = 'mp4').order_by('resolution').desc().first()
    audio_file = yt.streams.filter(only_audio=True).first()
    video_file.download('videos/')
    audio_file.download(output_path= 'audios/', mp3 = True)
    path = 'videos/' + yt.title + '.mp4'
    print(f"Path: {path}")
    return path

def crop_vertical(path):
    print(f"Cropping Video...")
    clip = mpy.VideoFileClip(path)

    (original_w,original_h) = clip.size
    new_w = int((9/16) * original_h )

    clip_cropped = crop(clip, width = new_w, height = original_h, x_center = int(original_w/2), y_center = int(original_h/2) )
    new_path = path.replace('.mp4', '_cropped_vert.mp4')    
    clip_cropped.write_videofile(new_path)

path = download_video('https://youtu.be/2dI9ql8KSH4?si=RuSB8HKz0auCCIXd')
crop_vertical(path)

def generate_subtitles(audio_file):
    # model = whisper.load_model("base.en")

    return 0

def split_video_into_minute():

    return 0

def run_clipper():

    return 0
