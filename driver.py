import ffmpeg_proxy as ffmpeg
import gtts_proxy as tts
import reddit_proxy as reddit
import youtube_proxy as yt
import proofread as pr

reddit_client = reddit.get_reddit_client(reddit.get_token_parameters())

posts = reddit.get_posts("AmITheAsshole", reddit_client, 10)
post = list(posts)[0]
tts.create_audio(pr.proofread(post.title), pr.proofread(post.selftext))
yt.download_video("https://www.youtube.com/watch?v=YwILPdVZsIY")
ffmpeg.merge_audio_and_video("video.mp4", "output.wav", "result.mp4")