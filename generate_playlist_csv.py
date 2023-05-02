import argparse
import csv
import youtube_dl

NO_URL = "no_url_supplied"
VIDEO_PLAYLIST_CSV_DEFAULT = "playlist.csv"

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--playlist_url", help="URL where the playlist is defined", type=str, default=NO_URL)

    parser.add_argument(
        "--playlist_csv", help="path for storing the video URLs", type=str, default=VIDEO_PLAYLIST_CSV_DEFAULT)

    parser.add_argument(
        "--verbose", help="debugging messages", action='store_true', default=False)

    return parser.parse_args()

def generate_playlist(url: str):
    
    # Set the options for youtube_dl
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'extract_flat': True,
        'get_id': True,
        'skip_download': True,
    }

    # Download the playlist information using youtube_dl
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(url, download=False)
        video_urls = [{"title": video["title"],
                       "url": f'https://www.youtube.com/watch?v={video["id"]}'}
                      for video in playlist_info['entries']]

    return video_urls

def write_playlist_as_csv(playlist: list, playlist_csv: str):
    with open(playlist_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Video title', 'Video URL'])
        for video in playlist:
            writer.writerow([video["title"], video["url"]])

def main(args: dict):
    # Set the playlist URL and the range of playlist items to download
    args.playlist_url = 'https://www.youtube.com/playlist?list=PLnUGmDYtaOMNGEUB5Gpq4bvUvoNyMlj2V'
    args.playlist_csv = "videos.csv"

    playlist = generate_playlist(args.playlist_url)
    write_playlist_as_csv(playlist, args.playlist_csv)

if __name__ == '__main__':
    flags = get_args()
    main(flags)

