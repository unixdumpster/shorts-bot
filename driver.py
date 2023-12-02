import os
import random as rand
import proxies.google_cloud_proxy as gcp
import proxies.video_builder as vb
import proxies.pollytts_proxy as pollytts
import utils.parse_content as pc
import utils.filemanager as fm

from dotenv import load_dotenv
from proxies import RedditClient
# setup
load_dotenv()
raw_video_dir, raw_audio_dir, final_product_dir = fm.setup()

# content
reddit_client = RedditClient(os.getenv('REDDIT_CLIENT_ID'),
                             os.getenv('REDDIT_CLIENT_SECRET'),
                             os.getenv('REDDIT_USERAGENT'))
post = reddit_client.get_post_and_screenshot()

# split post into multiple tuples of titles and texts
story_parts = pc.split_content(post, 180)
for part in story_parts:
    # audio
    audio_title = pollytts.create_audio(pc.proofread(part[0]), pc.proofread(part[1]))
    audio_path = os.path.join(raw_audio_dir, audio_title)

    # subtitles
    upload_audio_and_get_uri = gcp.upload_blob("shorts-bot-audio-bucket", audio_path, "audios/temp")
    gcs_response = gcp.long_running_recognize(upload_audio_and_get_uri)
    subtitles = gcp.get_transcript(gcs_response, 0.3)

    # video
    videos = os.listdir(raw_video_dir)
    video_type = videos[rand.randint(0, 2)]
    video_path = os.path.join(raw_video_dir, video_type)

    # product
    final_title = video_type.split(".")[0] + "_" + audio_title.split(".")[0].strip(" ") + "_FINAL.mp4"
    final_path = os.path.join(final_product_dir, final_title)
    vb.generate_video(video_path, audio_path, subtitles,
                      vb.generate_screenshot_overlay("screenshot.png", 3.5, video_path),
                      os.path.join(final_product_dir, final_title))

# cleanup
fm.teardown(raw_audio_dir, final_product_dir)
