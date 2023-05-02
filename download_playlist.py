#!python3

# This script merges two acquisition configuration files

import argparse
from colorama import Fore, Style
import csv
import os
import pytube as pt
from pytube.cli import on_progress

VIDEO_SAVE_DIR_DEFAULT = "videos"
NO_URL = "no_url_supplied"
NO_FILE = ""

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--video_url", help="URL where the video is downloaded from", type=str, default=NO_URL)

    parser.add_argument(
        "--playlist_csv", help="playlist file with all the URL to be downloaded", type=str, default=NO_FILE)

    parser.add_argument(
        "--video_save_dir", help="path for storing the video files", type=str, default=VIDEO_SAVE_DIR_DEFAULT)

    parser.add_argument(
        "--verbose", help="debugging messages", action='store_true', default=False)

    parser.add_argument(
        "--test", help="debugging messages", action='store_true', default=False)

    return parser.parse_args()

def create_dir(video_dirpath: str, verbose: bool):
    if os.path.exists(video_dirpath):
        if not os.path.isdir(video_dirpath):
            raise Exception(
                f"{video_dirpath} already exists and this is not a directory, please supply a directory")
    else:
        os.mkdir(video_dirpath)
        if verbose:
            print(f"The directory {video_dirpath} did not exist : created")

def download_video(video_url: str, output_folder=""):

    video=pt.YouTube(video_url,
                     use_oauth=True,
                     allow_oauth_cache=True,
                     on_progress_callback=on_progress)

    stream = video.streams.get_highest_resolution()
    print(stream)

    stream.download(output_folder)
    print()

def main(args: dict):
    
    create_dir(args.video_save_dir, args.verbose)
    
    if args.video_url != NO_URL:        
        video_url="https://youtube.com/watch?v=2lAe1cqCOXo" # youtube rewind
        video_url="https://youtu.be/u60pBuFEIdw" # spirou & fantasio
        
        download_video(video_url, args.video_save_dir)
        return
    
    if args.playlist_csv != NO_FILE:
        with open(args.playlist_csv, 'r') as csvfile:
            csvfile.readline() # skip header
            
            csv_rows = csv.reader(csvfile)
            for csv_row in csv_rows:
                download_video(csv_row[1], args.video_save_dir)

if __name__ == '__main__':
    flags = get_args()
    main(flags)
