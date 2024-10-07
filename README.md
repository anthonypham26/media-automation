# media-automation

### TikTok/Instagram Content Creation Automation Tool README
---
### Project Overview 

This Python project automates the entire video processing workflow, leveraging modern technologies to download a YouTube video, crop it to a vertical 9:16 aspect ratio, transcribe the audio using a high-performance machine learning model, generate time-stamped subtitle files, and seamlessly embed those captions back into the video. The solution integrates API interactions, audio-visual data manipulation, and natural language processing (NLP) techniques for end-to-end media automation. The final output is a fully captioned and formatted video, optimized for platforms requiring vertical video formats.

### Key Skills and Technologies:
- **Python**: Comprehensive use of Python for scripting and automation.
- **Machine Learning**: Audio transcription leveraging Whisper, a state-of-the-art ML model.
- **Natural Language Processing (NLP)**: Efficiently processes audio and generates accurate subtitles.
- **APIs & Automation**: Utilizes YouTube API to download video and audio streams.
- **Multimedia Processing**: Incorporates `ffmpeg` and `moviepy` for video editing, cropping, and caption embedding.
- **Data Manipulation**: Formats timestamps and manages text input/output for .srt subtitle generation.
- **Performance Optimization**: Employs efficient data handling and external libraries (like `ffmpeg`) to ensure optimized video and audio processing.

#### Script Components

1. **`download_video(url)`**:
   - Downloads the video and audio streams from a YouTube URL.
   - Saves the video to the `videos/` folder and the audio to the `audios/` folder in `.mp3` format.

2. **`crop_vertical(path)`**:
   - Crops the video to a vertical 9:16 aspect ratio, keeping the original height and adjusting the width.
   - Saves the cropped video as `_cropped_vert.mp4` in the same folder.

3. **`transcribe_video(audio_file)`**:
   - Uses the `faster-whisper` model to transcribe the audio file, returning word-level transcription segments with timestamps.

4. **`generate_subtitles_file(audio_file, segments, words_per_chunk=3)`**:
   - Creates a `.srt` subtitle file by grouping words from the transcription into chunks of 3 words.
   - Writes each group with start and end timestamps into the subtitle file.

5. **`embed_captions_to_video(video_path, audio_path, srt_path, output_path)`**:
   - Embeds the generated subtitles into the video with customized styling (font, color, outline, and karaoke effect).
   - Combines the video and audio, and saves the result as a new file.

6. **`clear_folder(folder_path)`**:
   - Clears out the specified folder (`audios/`, `videos/`, etc.) by deleting its contents.

7. **`run_clipper()`**:
   - The main function that:
     1. Takes a YouTube URL as input.
     2. Downloads the video and audio.
     3. Crops the video to a vertical aspect ratio.
     4. Transcribes the audio and generates subtitle files.
     5. Embeds the subtitles into the video and saves the final output.
     6. Clears the `audios/` and `videos/` folders after processing.

#### How to Use

1. **Clone the Repository**: 
   If using a GitHub repository, clone the repo and navigate into the project folder.
   ```bash
   git clone https://github.com/your-repo/media-automation.git
   cd media-automation
   ```
2. **Install Dependencies**:
   - Install the required libraries from the `requirements.txt` file using the following command:

   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Script**:
   - Run the Python script and enter a YouTube URL when prompted.
   ```bash
   python clipper.py
   ```
4. **Output**:
   - The processed video (cropped and with embedded subtitles) will be saved in the `output/` folder.

#### Customization

- **Subtitle Styling**: You can modify the subtitle appearance (font, color, alignment, etc.) by adjusting the `force_style` string in the `embed_captions_to_video` function.
- **Subtitle Grouping**: Change the number of words per subtitle by adjusting the `words_per_chunk` parameter in the `generate_subtitles_file` function.

#### License

This project is open-source and available under the [MIT License](LICENSE).


