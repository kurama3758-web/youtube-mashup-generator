import os
import shutil
from yt_dlp import YoutubeDL
from pydub import AudioSegment

def generate_mashup(singer, num_videos, duration, output_file):
    os.makedirs("audios", exist_ok=True)
    os.makedirs("trimmed", exist_ok=True)

    # Download audio directly
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audios/%(id)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch{num_videos}:{singer} songs"])

    # Trim
    for file in os.listdir("audios"):
        if file.endswith(".mp3"):
            audio = AudioSegment.from_file(os.path.join("audios", file))
            trimmed = audio[:duration * 1000]
            trimmed.export(os.path.join("trimmed", file), format="mp3")

    # Merge
    combined = AudioSegment.empty()
    for file in os.listdir("trimmed"):
        combined += AudioSegment.from_file(os.path.join("trimmed", file))

    combined.export(output_file, format="mp3")

    # Cleanup temp folders
    shutil.rmtree("audios", ignore_errors=True)
    shutil.rmtree("trimmed", ignore_errors=True)

    return output_file
