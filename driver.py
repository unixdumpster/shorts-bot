import proxies.ffmpeg_proxy as ffmpeg
import proxies.pollytts_proxy as pollytts
import proxies.reddit_proxy as reddit
import proofread as pr
import os
import random as rand

# content
reddit_client = reddit.get_reddit_client(reddit.get_token_parameters())
posts = reddit.get_posts("AmITheAsshole", reddit_client, 10)
post = list(posts)[0]

# audio
audio_path = os.path.join(os.getcwd(), 'raw_audios')
audio_title = pollytts.create_audio(pr.proofread(post.title), pr.proofread(post.selftext))
audio_path = os.path.join(audio_path, audio_title)


# video
video_path = os.path.join(os.getcwd(), 'raw_videos')
videos = os.listdir(video_path)
video_type = videos[rand.randint(0, 2)]
video_path = os.path.join(video_path, video_type)

# # product
final_title = video_type.split(".")[0] + "_" + audio_title.split(".")[0].strip(" ") + "_FINAL.mp4"
print(final_title)
ffmpeg.merge_audio_and_video(video_path, audio_path, os.path.join('final_products', final_title))