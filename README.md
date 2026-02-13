# YouTube Mashup Generator

A Flask-based web application that generates a mashup of YouTube songs based on user input and sends the generated file via email.

---

## Project Description

This application allows a user to:

1. Enter a singer name.
2. Specify the number of videos.
3. Define the duration (in seconds) for each clip.
4. Provide an email address.

The system searches YouTube, downloads the requested number of audio files, trims each to the specified duration, merges them into a single mashup file, compresses the output, and sends it to the user's email.

---

## Features

- Search YouTube videos by singer name
- Download audio using yt-dlp
- Trim audio to fixed duration
- Merge multiple clips into a single mashup
- Compress output into a ZIP file
- Send mashup via Gmail SMTP
- Web interface built using Flask

---

## Tech Stack

- Python 3.10
- Flask
- yt-dlp
- pydub
- FFmpeg
- python-dotenv
- smtplib

---

## Project Structure

