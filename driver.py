import proxies.ffmpeg_proxy as ffmpeg
import proxies.pollytts_proxy as pollytts
import proxies.reddit_proxy as reddit
import proofread as pr
import os
import random as rand
import proxies.google_cloud_proxy as transcribe

# content
reddit_client = reddit.get_reddit_client(reddit.get_token_parameters())
posts = reddit.get_posts("AmITheAsshole", reddit_client, 10)
post = list(posts)[2]

# audio
audio_path = os.path.join(os.getcwd(), 'raw_audios')
audio_title = pollytts.create_audio(pr.proofread(post.title), pr.proofread(post.selftext))
audio_path = os.path.join(audio_path, audio_title)

#subtitles
upload_audio_and_get_uri = transcribe.upload_blob("shorts-bot-audio-bucket", audio_path, "audios/temp.wav")
gcs_response = transcribe.long_running_recognize(upload_audio_and_get_uri)
subtitles = transcribe.get_transcript(gcs_response, 0.3)

# video
video_path = os.path.join(os.getcwd(), 'raw_videos')
videos = os.listdir(video_path)
video_type = videos[rand.randint(0, 2)]
video_path = os.path.join(video_path, video_type)

# product
final_title = video_type.split(".")[0] + "_" + audio_title.split(".")[0].strip(" ") + "_FINAL.mp4"
print(final_title)
final_path = os.path.join('final_products', final_title)
ffmpeg.generate_video(video_path, audio_path, subtitles, os.path.join('final_products', final_title))