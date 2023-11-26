import proxies.video_builder as vb
import proxies.pollytts_proxy as pollytts
from proxies import RedditClient
import os
import random as rand
import proxies.google_cloud_proxy as gcp
from dotenv import load_dotenv
import utils.proofread as pr 

load_dotenv()
# content
reddit_client = RedditClient(os.getenv('REDDIT_CLIENT_ID'),
                             os.getenv('REDDIT_CLIENT_SECRET'),
                             os.getenv('REDDIT_USERAGENT'))

post = list(reddit_client.get_posts_and_screenshots(1).keys())[0]
    
# audio
audio_path = os.path.join(os.getcwd(), 'raw_audios')
audio_title = pollytts.create_audio(pr.proofread(post.title), pr.proofread(post.selftext))
audio_path = os.path.join(audio_path, audio_title)

# subtitles
upload_audio_and_get_uri = gcp.upload_blob("shorts-bot-audio-bucket", audio_path, "audios/temp")
gcs_response = gcp.long_running_recognize(upload_audio_and_get_uri)
subtitles = gcp.get_transcript(gcs_response, 0.3)

# video
video_path = os.path.join(os.getcwd(), 'raw_videos')
videos = os.listdir(video_path)
video_type = videos[rand.randint(0, 2)]
video_path = os.path.join(video_path, video_type)

# product
final_title = video_type.split(".")[0] + "_" + audio_title.split(".")[0].strip(" ") + "_FINAL.mp4"
print(final_title)
final_path = os.path.join('final_products', final_title)
vb.generate_video(video_path, audio_path, subtitles, os.path.join('final_products', final_title))
