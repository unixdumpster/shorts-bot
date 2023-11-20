from pytube import YouTube

def download_video(url):
    yt = YouTube(url)
    video_stream = yt.streams.get_highest_resolution()
    video_stream.download(filename="video.mp4")