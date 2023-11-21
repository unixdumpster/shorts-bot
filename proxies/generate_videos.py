import os
import pytube
import time 

hm_videos = {'CSGO': 'https://www.youtube.com/watch?v=Lixl3-jz7k8', 
            'MC': 'https://www.youtube.com/watch?v=intRX7BRA90', 
            'GTA': 'https://www.youtube.com/watch?v=VB0zDS9ITmk'}

titles = hm_videos.keys()
urls = hm_videos.values()

start = time.time()

for title, url in zip(titles, urls):
    # creates a directory 'raw_videos' at the same level as the proxies folder
    parent_path = os.path.dirname(os.getcwd())
    path = os.path.join(parent_path, "raw_videos")

    if os.path.exists(path):
        break

    os.mkdir(path)

    yt = pytube.YouTube(url)
    video = yt.streams.get_highest_resolution()
    video.download(output_path = path, filename=f"{title}.mp4")

end = time.time()
print("Total seconds elapsed: ", end - start)


