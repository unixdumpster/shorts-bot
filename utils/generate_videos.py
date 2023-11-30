import pytube


def generate_videos(output_path):
    hm_videos = {'CSGO': 'https://www.youtube.com/watch?v=Lixl3-jz7k8',
                 'MC': 'https://www.youtube.com/watch?v=intRX7BRA90',
                 'GTA': 'https://www.youtube.com/watch?v=VB0zDS9ITmk'}

    titles = hm_videos.keys()
    urls = hm_videos.values()

    for title, url in zip(titles, urls):
        yt = pytube.YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download(output_path=output_path, filename=f"{title}.mp4")


