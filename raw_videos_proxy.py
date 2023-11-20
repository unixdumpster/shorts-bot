import os
import pytube
from dotenv import load_dotenv
from time import time

load_dotenv()

hm_videos = {'CSGO': 'https://www.youtube.com/watch?v=Lixl3-jz7k8', 
                'MC': 'https://www.youtube.com/watch?v=intRX7BRA90', 
                'GTA': 'https://www.youtube.com/watch?v=VB0zDS9ITmk'}

titles = hm_videos.keys()
urls = hm_videos.values()

start = time()
for title, url in zip(titles, urls):
    yt = pytube.YouTube(url)
    video = yt.streams.get_highest_resolution()
    path = os.getcwd() + os.getenv("RAW_VIDEOS_DIR")
    video.download(output_path = path, filename=f"{title}.mp4")
end = time()

print("Total seconds elapsed: ", end - start)