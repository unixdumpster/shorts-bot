import random
from moviepy.editor import *

def generate_video(video_path, audio_path, subtitles, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    # Calculate the valid range for the start point of the video
    valid_start_range = (0, video_clip.duration - audio_clip.duration)

    # Set a random start point within the valid range
    start_time = random.uniform(valid_start_range[0], valid_start_range[1])

    # Cut the video to match the length of the audio starting from the random start point
    video_clip = video_clip.subclip(start_time, start_time + audio_clip.duration)
    
    video_clip = video_clip.set_audio(audio_clip)

    # Create a TextClip object for each subtitle and set the duration
    subtitle_clips = []
    for (start, end), text in subtitles:
        subtitle_clip = TextClip(text, fontsize=60, color='white', font='Impact', stroke_color='purple',stroke_width=2)
        subtitle_clip = subtitle_clip.set_pos('center').set_duration(end - start).set_start(start)
        # subtitle_clip = subtitle_clip.resize(lambda t: resize(t, (end - start) / 2))
        
        subtitle_clips.append(subtitle_clip)

    # Overlay the subtitle clips on the video
    final_clip = CompositeVideoClip([video_clip] + subtitle_clips)

    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    video_clip.close()
    audio_clip.close()
    final_clip.close()

def resize(t, duration):
    if duration == 0:
        return 1
    # Starting scale factor
    start_scale = 1
    # End scale factor (the size to which the text should grow)
    end_scale = 1.1
    # Calculate the scaling factor based on elapsed time and total duration
    scale_factor = start_scale + t/duration * (end_scale - start_scale)
    return scale_factor
