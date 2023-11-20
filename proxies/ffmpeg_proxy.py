import random
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.config import change_settings
import re

def merge_audio_and_video(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    # Calculate the valid range for the start point of the video
    valid_start_range = (0, video_clip.duration - audio_clip.duration)

    # Set a random start point within the valid range
    start_time = random.uniform(valid_start_range[0], valid_start_range[1])

    # Cut the video to match the length of the audio starting from the random start point
    video_clip = video_clip.subclip(start_time, start_time + audio_clip.duration)
    
    video_clip = video_clip.set_audio(audio_clip)

    video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    video_clip.close()
    audio_clip.close()