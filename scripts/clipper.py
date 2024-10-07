import os
from pytubefix import YouTube
import ffmpeg
import moviepy.editor as mpy
from moviepy.video.fx.all import crop
from faster_whisper import WhisperModel
import math
import shutil

# input: youtube url, outputs into videos/ and audios/
def download_video(url):
    yt = YouTube(url)
    print(f"Downloading {yt.title} from Youtube")
    video_file = yt.streams.filter(only_video= True, file_extension = 'mp4').order_by('resolution').desc().first()
    audio_file = yt.streams.filter(only_audio=True).first()
    video_file.download('videos/')
    audio_file.download(output_path= 'audios/', mp3 = True)
    path = 'videos/' + yt.title + '.mp4'
    return path

# crops a video to a vertical aspect ratio (9:16) by adjusting the width while keeping the original height centered
def crop_vertical(path):
    print(f"Cropping Video...")
    clip = mpy.VideoFileClip(path)

    (original_w,original_h) = clip.size
    new_w = int((9/16) * original_h )

    clip_cropped = crop(clip, width = new_w, height = original_h, x_center = int(original_w/2), y_center = int(original_h/2) )
    new_path = path.replace('.mp4', '_cropped_vert.mp4')    
    clip_cropped.write_videofile(new_path)
    return new_path

#uses faster-Whisper model to transcribe an audio file, returning word-level transcription segments with timestamps
def transcribe_video(audio_file):
    model = WhisperModel("base.en", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_file, word_timestamps=True)
    language = info[0]
    print(f"Language: {language}")
    segments = list(segments)
    # for segment in segments:
    #     for word in segment.words:
    #         print("[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))
    return segments

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

#generates a timestamped .srt file by grouping words from segments into chunks based on the specified number
def generate_subtitles_file(audio_file, segments, words_per_chunk=3):
    subtitles_file = f"{audio_file}_captioned.srt"
    text = ""
    subtitle_index = 0
    for segment in segments:
        current_start = segment.start
        grouped_text = ""
        word_count = 0
        for word in segment.words:
            if current_start is None:
                current_start = word.start
            current_end = word.end
            grouped_text += " " + word.word
            word_count += 1
            if word_count >= words_per_chunk:
                # Write the current chunk to the subtitles
                subtitle_index += 1
                text += f"{str(subtitle_index)}\n"
                text += f"{format_time(current_start)} --> {format_time(current_end)}\n"
                text += f"{grouped_text.strip()}\n\n"
                # Reset the grouping and update the current start time
                grouped_text = ""
                word_count = 0
                current_start = word.end
        # Write any remaining words that didn't reach the word limit
        if grouped_text.strip():
            subtitle_index += 1
            text += f"{str(subtitle_index)}\n"
            text += f"{format_time(current_start)} --> {format_time(current_end)}\n"
            text += f"{grouped_text.strip()}\n\n"
    with open(subtitles_file, 'w') as f:
        f.write(text)
    return subtitles_file

#embeds the subtitles into the video with customized styling and saves the output
def embed_captions_to_video(video_path, audio_path, srt_path, output_path):
    video = ffmpeg.input(video_path)
    captioned_video = ffmpeg.filter(video,'subtitles', srt_path, force_style='FontName=Arial Black,PrimaryColour=&H00FFFFFF,Outline=2,Karaoke=1,Italic=1,Alignment=10')
    audio = ffmpeg.input(audio_path)
    output = ffmpeg.output(captioned_video, audio, output_path, vcodec='libx264', acodec='aac' )
    ffmpeg.run(output, overwrite_output=True)                       

def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def run_clipper():
    url = str(input("Enter a Youtube Url:"))
    vid = download_video(url)
    vid_title = YouTube(url).title
    new_vid = crop_vertical(vid)
    audio_path = "audios/" + vid_title + ".mp3"
    segments = transcribe_video(audio_path)
    srt_path= generate_subtitles_file(audio_path, segments)
    output_path = "output/" + vid_title + "cropped_captioned.mp4"
    embed_captions_to_video(new_vid, audio_path, srt_path, output_path)
    #clear out working folders
    clear_folder('audios')
    clear_folder('videos')

run_clipper()

# clear_folder('output')

# def split_video_into_minute():
#     return 0

#'https://youtu.be/dOuNLS1elWs?si=3fheYEeVwhhJft7s'