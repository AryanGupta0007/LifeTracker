import yt_dlp
from moviepy.editor import VideoFileClip
import os
import time
from pathlib import Path
import shutil


def download_youtube_video(url, downloads_folder):
    output_path = f'./{downloads_folder}'
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'noplaylist': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print('Download completed!')
    except Exception as e:
        print(f'Error: {e}')

def convert_file_to_mp3(files, donwloads_folder_path, mp3_files_path):
    os.chdir(donwloads_folder_path)
    print(donwloads_folder_path)
    file_names = files.keys()
    for file_name in file_names:
        file_extension = files[file_name]
        video_file_path = os.path.join(donwloads_folder_path, f"{file_name}{file_extension}")
        # Path to save the MP3 file
        mp3_file_path = os.path.join(mp3_files_path, f"{file_name}.mp3")
        # Load the video file
        video = VideoFileClip(video_file_path)
        # Extract the audio and save it as an MP3 file
        video.audio.write_audiofile(mp3_file_path)
        print(f'Converted {video_file_path} to {mp3_file_path}')
    os.chdir("..")
    return files

def get_audio_file(file, downloads_path):
    print(f"audio path: {downloads_path}")
    with open(str(file), 'rb') as audio:
        print("audio")
    return audio

def create_zip_folder(folder):
    folder_path = os.getcwd() + rf'\{folder}'
    print(f"folder: {folder_path}")
    output_zip_path = folder
    shutil.make_archive(output_zip_path, 'zip', folder_path)


def delete_file(file):
    os.remove(file)


def get_files_and_extensions(folder):
    directory = r'./' + folder   # downloads directory
    files = {}
    for file in os.listdir(directory):
        name, ext = os.path.splitext(file)
        files[name] = ext
    return files


def get_file_extension(file_name):
    files = get_files_and_extensions()
    extension = files[file_name]
    return extension

def get_audio(links, current_user):
    downloads_folder_path = os.getcwd() + r"\downloads" + f"_{current_user['id']}"
    mp3_files_path = os.getcwd() + r"\mp3_files" + f"_{current_user['id']}"
    downloads_folder = f"downloads_{current_user['id']}"
    mp3_folder = f"mp3_files_{current_user["id"]}"
    os.mkdir(downloads_folder)
    os.mkdir(mp3_folder)
    for link in links:
        download_youtube_video(url=link, downloads_folder=downloads_folder)
    files = get_files_and_extensions(folder=downloads_folder)
    convert_file_to_mp3(files=files, donwloads_folder_path=downloads_folder_path, mp3_files_path=mp3_files_path)


def delete_folders_and_files_previously_created():
    user_ids = range(1, 100)
    directory = '.'
    for user_id in user_ids:
        for file in os.listdir(directory):
            if file == f"downloads_{user_id}":
                shutil.rmtree(file)
            elif file == f"mp3_files_{user_id}":
                shutil.rmtree(file)
            elif file == f"mp3_files_{user_id}.zip":
                os.remove(file)

def delete_dumb_user_folders_and_files_previously_created():
    user_id = 0
    directory = "."
    for file in os.listdir(directory):
        if file == f"downloads_{user_id}":
            shutil.rmtree(file)
        elif file == f"mp3_files_{user_id}":
            shutil.rmtree(file)
        elif file == f"mp3_files_{user_id}.zip":
            os.remove(file)

def while_away_time():
    file_path = os.getcwd() + r'/while_away.txt'
    # Open the file and read each line
    with open(file_path, 'r') as file:
        for line in file:
            print(line.strip())  # strip() removes any leading/trailing whitespace


