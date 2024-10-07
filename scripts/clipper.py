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

# segments = transcribe_video("audios/ICYMI — Apple Event Highlights.mp3")
# generate_subtitles_file("audios/ICYMI — Apple Event Highlights.mp3",segments)

# def embed_captions_to_video(video_file, audio_file, subtitle_file, output_file):
# Step 1: Add subtitles to the video
# video_with_subtitles = ffmpeg.input('videos/ICYMI — Apple Event Highlights_cropped_vert.mp4')
# video_with_subtitles = ffmpeg.filter(video_with_subtitles, 'subtitles', 'audios/ICYMI — Apple Event Highlights.mp3_captioned.srt')

# # Step 2: Add audio to the video (with subtitles)
# audio_input_stream = ffmpeg.input('audios/ICYMI — Apple Event Highlights.mp3')

# # Step 3: Concatenate the video (with subtitles) and audio together
# output = ffmpeg.concat(video_with_subtitles, audio_input_stream, v=1, a=1)

# # Step 4: Run the ffmpeg command
# ffmpeg.run(output, overwrite_output=True)

# print(f"Captions and audio embedded successfully into {output_file}")


# Step 1: Add subtitles to the video
video_input_stream = ffmpeg.input('videos/ICYMI — Apple Event Highlights_cropped_vert.mp4')
subtitle_input_stream = 'audios/ICYMI — Apple Event Highlights.mp3_captioned.srt'  # subtitle file
video_with_subtitles = ffmpeg.filter(video_input_stream, 'subtitles', subtitle_input_stream)

# Step 2: Add audio to the video (with subtitles)
audio_input_stream = ffmpeg.input('audios/ICYMI — Apple Event Highlights.mp3')

# Step 3: Combine video (with subtitles) and audio together by explicitly mapping streams
output_video = 'output/ICYMI_Apple_Event_Highlights_captioned_output.mp4'
ffmpeg_output = (
    ffmpeg
    .output(
        video_with_subtitles, 
        audio_input_stream, 
        output_video, 
        vcodec='libx264',  # Re-encode video using libx264 codec
        acodec='aac',  # Encode audio as AAC
        strict='experimental',
        shortest=None  # Ensure the shortest duration is respected, to avoid desync issues
    )
    .run(overwrite_output=True)
)

print(f"Video with audio and subtitles has been successfully processed: {output_video}")





    
# path = download_video('https://youtu.be/Oh79ZsPLo7U?si=-79rBA3ugRJF7Gqc')
# crop_vertical(path)

# generate_subtitles("audios/ICYMI — Apple Event Highlights.mp3")



def split_video_into_minute():

    return 0

def run_clipper():

    return 0
