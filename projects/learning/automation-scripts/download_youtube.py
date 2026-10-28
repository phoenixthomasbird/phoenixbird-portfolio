
from pytube import YouTube

def download_video(url):
    yt = YouTube(url)
    yt.streams.get_highest_resolution().download()
    print("Video downloaded successfully.")

download_video("https://www.youtube.com/watch?v=example")

