import yt_dlp
from moviepy.editor import VideoFileClip
import os
import time
from pathlib import Path
import shutil


def download_youtube_video(url, output_path='./downloads'):
    os.mkdir(f'downloads')
    os.mkdir(f'mp3_files')
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print('Download completed!')
    except Exception as e:
        print(f'Error: {e}')

def convert_file_to_mp3(files, path=os.getcwd() + "\downloads"):
    mp3_files_path = os.getcwd() + r"\mp3_files"
    downloads_path = os.getcwd() + r"\downloads"
    os.chdir(path)
    print(path)
    file_names = files.keys()
    for file_name in file_names:
        file_extension = files[file_name]

        video_file_path = os.path.join(downloads_path, f"{file_name}{file_extension}")

        # Path to save the MP3 file
        mp3_file_path = os.path.join(mp3_files_path, f"{file_name}.mp3")

        # Load the video file
        video = VideoFileClip(video_file_path)

        # Extract the audio and save it as an MP3 file
        video.audio.write_audiofile(mp3_file_path)
        print(f'Converted {video_file_path} to {mp3_file_path}')
    return files

def get_audio_file(file, path=os.getcwd() + "\downloads"):
    print(f"audio path: {path}")
    with open(str(file), 'rb') as audio:
        print("audio")
    return audio

def create_zip_folder():

    folder_path = os.getcwd() + r"\mp3_files"
    print(f"folder: {folder_path}")
    output_zip_path = "mp3_files"
    shutil.make_archive(output_zip_path, 'zip', folder_path)

def delete_file(file):
    os.remove(file)

def get_files_and_extensions():
    directory = './downloads'  # downloads directory
    files = {}
    for file in os.listdir(directory):
        name, ext = os.path.splitext(file)
        files[name] = ext
    return files


def get_file_extension(file_name):
    files = get_files_and_extensions()
    extension = files[file_name]
    return extension

def get_audio(links):
    for link in links:
        download_youtube_video(link)
    files = get_files_and_extensions()
    files = convert_file_to_mp3(files=files)
    return files


def create_zip_for_user():
    create_zip_folder()



