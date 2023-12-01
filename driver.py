import proxies.video_builder as vb
import proxies.pollytts_proxy as pollytts
from proxies import RedditClient
import os
import random as rand
import proxies.google_cloud_proxy as gcp
from dotenv import load_dotenv
import utils.parse_content as pc
import utils.generate_videos as gv

# setup
load_dotenv()

raw_video_path = os.path.join(os.getcwd(), 'raw_videos')
if not os.path.exists(raw_video_path):
    os.mkdir(raw_video_path)
    gv.generate_videos(raw_video_path)

raw_audio_path = os.path.join(os.getcwd(), 'raw_audios')
if not os.path.exists(raw_audio_path):
    os.mkdir(raw_audio_path)

# content
reddit_client = RedditClient(os.getenv('REDDIT_CLIENT_ID'),
                             os.getenv('REDDIT_CLIENT_SECRET'),
                             os.getenv('REDDIT_USERAGENT'))

post = list(reddit_client.get_posts_and_screenshots(1).keys())[0]

# split post into multiple tuples of titles and texts
story_parts = pc.split_content(post, 180)
for part in story_parts:
    # audio
    audio_title = pollytts.create_audio(pc.proofread(part[0]), pc.proofread(part[1]))
    audio_path = os.path.join(raw_audio_path, audio_title)

    # subtitles
    upload_audio_and_get_uri = gcp.upload_blob("shorts-bot-audio-bucket", audio_path, "audios/temp")
    gcs_response = gcp.long_running_recognize(upload_audio_and_get_uri)
    subtitles = gcp.get_transcript(gcs_response, 0.3)

    # video
    videos = os.listdir(raw_video_path)
    video_type = videos[rand.randint(0, 2)]
    video_path = os.path.join(raw_video_path, video_type)

    # product
    final_title = video_type.split(".")[0] + "_" + audio_title.split(".")[0].strip(" ") + "_FINAL.mp4"
    print(final_title)
    final_path = os.path.join('final_products', final_title)
    vb.generate_video(video_path, audio_path, subtitles, vb.generate_screenshot_overlay("screenshot.png", 3.5, video_path), os.path.join('final_products', final_title))

# cleanup
audio_files = os.listdir(raw_audio_path)
for audio_file in audio_files:
    audio_file_path = os.path.join(raw_audio_path, audio_file)
    if os.path.isfile(audio_file_path):
        os.remove(audio_file_path)

try:
    os.rmdir(raw_audio_path)
except OSError as error:
    print(error)
