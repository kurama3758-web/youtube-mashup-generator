import sys
import os
import shutil
from yt_dlp import YoutubeDL
from moviepy import VideoFileClip
from pydub import AudioSegment


# ----------------------------
# Validate Command Line Inputs
# ----------------------------
def validate_inputs():
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer = sys.argv[1]
    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        print("Error: NumberOfVideos and AudioDuration must be integers.")
        sys.exit(1)

    output_file = sys.argv[4]

    if num_videos <= 10:
        print("Error: NumberOfVideos must be greater than 10.")
        sys.exit(1)

    if duration <= 20:
        print("Error: AudioDuration must be greater than 20 seconds.")
        sys.exit(1)

    if not output_file.endswith(".mp3"):
        print("Error: Output file must be .mp3 format.")
        sys.exit(1)

    return singer, num_videos, duration, output_file


# ----------------------------
# Download Videos from YouTube
# ----------------------------
def download_and_convert(singer, num_videos):
    print("Downloading audio directly...")

    os.makedirs("audios", exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audios/%(id)s.%(ext)s',
        'noplaylist': True,
        'quiet': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch{num_videos}:{singer} songs"])
    except Exception as e:
        print("Error downloading audio:", e)
        sys.exit(1)


# ----------------------------
# Trim First Y Seconds
# ----------------------------
def trim_audios(duration):
    print("Trimming audio files...")
    os.makedirs("trimmed", exist_ok=True)

    try:
        for file in os.listdir("audios"):
            audio = AudioSegment.from_mp3(os.path.join("audios", file))
            trimmed_audio = audio[:duration * 1000]  # milliseconds
            trimmed_audio.export(os.path.join("trimmed", file), format="mp3")
    except Exception as e:
        print("Error trimming audio:", e)
        sys.exit(1)


# ----------------------------
# Merge All Audios
# ----------------------------
def merge_audios(output_file):
    print("Merging audio files...")

    combined = AudioSegment.empty()

    try:
        for file in os.listdir("trimmed"):
            audio = AudioSegment.from_mp3(os.path.join("trimmed", file))
            combined += audio

        combined.export(output_file, format="mp3")
        print(f"\nMashup created successfully: {output_file}")

    except Exception as e:
        print("Error merging audio:", e)
        sys.exit(1)


# ----------------------------
# Clean Temporary Folders
# ----------------------------
def cleanup():
    shutil.rmtree("videos", ignore_errors=True)
    shutil.rmtree("audios", ignore_errors=True)
    shutil.rmtree("trimmed", ignore_errors=True)


# ----------------------------
# MAIN FUNCTION
# ----------------------------
def main():
    singer, num_videos, duration, output_file = validate_inputs()

    download_and_convert(singer, num_videos)
    trim_audios(duration)
    merge_audios(output_file)
    cleanup()


if __name__ == "__main__":
    main()
