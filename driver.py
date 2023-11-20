import proxies.ffmpeg_proxy as ffmpeg
import proxies.pollytts_proxy as pollytts
import proxies.gtts_proxy as tts
import proxies.reddit_proxy as reddit
import proxies.youtube_proxy as yt
import proofread as pr
import os

reddit_client = reddit.get_reddit_client(reddit.get_token_parameters())

posts = reddit.get_posts("AmITheAsshole", reddit_client, 10)
post = list(posts)[0]
pollytts.create_audio(pr.proofread(post.title), pr.proofread(post.selftext))
# tts.create_audio(pr.proofread(post.title), pr.proofread(post.selftext))
# yt.download_video("https://www.youtube.com/watch?v=YwILPdVZsIY")

video_path = os.getcwd() + "\\raw_videos\\CSGO.mp4"
audio_path = os.getcwd() + "\\raw_audios\\AITA.mp3"
ffmpeg.merge_audio_and_video(video_path, audio_path, "video_MVP.mp4")