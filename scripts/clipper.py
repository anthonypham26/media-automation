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

# download_video('https://youtu.be/dOuNLS1elWs?si=3fheYEeVwhhJft7s')

def crop_vertical(path):
    print(f"Cropping Video...")
    clip = mpy.VideoFileClip(path)

    (original_w,original_h) = clip.size
    new_w = int((9/16) * original_h )

    clip_cropped = crop(clip, width = new_w, height = original_h, x_center = int(original_w/2), y_center = int(original_h/2) )
    new_path = path.replace('.mp4', '_cropped_vert.mp4')    
    clip_cropped.write_videofile(new_path)

# crop_vertical('videos/Hearing Aid feature for AirPods Pro 2  Apple.mp4')

from faster_whisper import WhisperModel

def transcribe_video(audio_file):
    model = WhisperModel("base.en", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_file)
    language = info[0]
    print(f"Language: {language}")
    segments = list(segments)
    for segment in segments :
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

    return segments

import math
#HH:MM:SS,sss
def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours :02d}:{minutes :02d}:{seconds :02d},{milliseconds :03d}"
    return formatted_time

def generate_subtitles_file(audio_file, segments):
    subtitles_file = f"{audio_file}_captioned.srt"
    text = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment.start)
        segment_end = format_time(segment.end)
        text += f"{str(index + 1)}\n"
        text += f"{segment_start} --> {segment_end}\n"
        text += f"{segment.text}\n\n"
    f = open(subtitles_file, 'w')
    f.write(text)
    f.close
    return subtitles_file

# segments = transcribe_video("audios/Hearing Aid feature for AirPods Pro 2  Apple.mp3")
# generate_subtitles_file("audios/Hearing Aid feature for AirPods Pro 2  Apple.mp3",segments)


def embed_captions_to_video(video_path, audio_path, srt_path):
    print(video_path)
    video = ffmpeg.input(video_path)
    print(srt_path)
    captioned_video = ffmpeg.filter(video,'subtitles', srt_path)
    print(audio_path)
    audio = ffmpeg.input(audio_path)
    # output_path = "output/" + 
    # output = ffmpeg.output(captioned_video, audio, , vcodec='libx264', acodec='aac )
    ffmpeg.run(output, overwrite_output=True)                       





# video_with_subtitles = ffmpeg.input('videos/Hearing Aid feature for AirPods Pro 2  Apple.mp4')
# video_with_subtitles = ffmpeg.filter(video_with_subtitles, 'subtitles', 'audios/Hearing Aid feature for AirPods Pro 2  Apple.mp3_captioned.srt')


# audio_input_stream = ffmpeg.input('audios/Hearing Aid feature for AirPods Pro 2  Apple.mp3')

# output = ffmpeg.output(video_with_subtitles, audio_input_stream, 'output/Hearing_Aid_feature_with_audio_and_subtitles.mp4', vcodec='libx264', acodec='aac')

# ffmpeg.run(output, overwrite_output=True)





# # # Step 1: Add subtitles to the video
# video_input_stream = ffmpeg.input('videos/ICYMI — Apple Event Highlights_cropped_vert.mp4')
# subtitle_input_stream = 'audios/ICYMI — Apple Event Highlights.mp3_captioned.srt'  # subtitle file
# video_with_subtitles = ffmpeg.filter(video_input_stream, 'subtitles', subtitle_input_stream)

# ffmpeg.concat(video_input_stream, subtitle_input_stream, v=1, a=1)


# def merge_video_audio(input_video, input_audio, output_file):
#     # Add quotes around file paths to handle spaces or special characters
#     # ffmpeg -i silent.mp4 -i music.mp3 -map 0:v -map 1:a -c copy video_with_music.mp4

#     command = f'ffmpeg -i "{input_video}" -i "{input_audio}" -map 0:v -map 1:a? -c copy "{output_file}"'
#     os.system(command)



# command = f'ffmpeg -i "videos/Hearing Aid feature for AirPods Pro 2  Apple.mp4" -i "audios/Hearing Aid feature for AirPods Pro 2  Apple.mp3" -c:v copy -c:a aac "output/Hearing_Aid_feature_for_AirPods_Pro_2_Apple_output.mp4"'
# os.system(command)

# ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac output.mp4


    
# path = download_video('https://youtu.be/Oh79ZsPLo7U?si=-79rBA3ugRJF7Gqc')
# crop_vertical(path)

# generate_subtitles("audios/ICYMI — Apple Event Highlights.mp3")



def split_video_into_minute():

    return 0

def run_clipper():

    return 0
