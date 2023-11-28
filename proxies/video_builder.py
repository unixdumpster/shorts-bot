import random
from moviepy.editor import *

def generate_video(video_path, audio_path, subtitles, screenshot_clips, output_path):
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
        subtitle_clip = TextClip(text, fontsize=50, color='white', font='Impact', stroke_color='purple',stroke_width=2)
        subtitle_clip = subtitle_clip.set_pos('center').set_duration(end - start).set_start(start)
        # subtitle_clip = subtitle_clip.resize(lambda t: resize(t, (end - start) / 2))
        
        subtitle_clips.append(subtitle_clip)

    # Overlay the clips together
    final_clip = CompositeVideoClip([video_clip] + subtitle_clips + screenshot_clips).crop(x_center=video_clip.w / 2, width=550)

    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    video_clip.close()
    audio_clip.close()
    final_clip.close()

def generate_screenshot_overlay(image_path, end_time, video_path):
    overlay_image = ImageClip(image_path).set_pos('center')
    overlay_image = overlay_image.resize(width=overlay_image.size[0] / 1.15, height=overlay_image.size[1] / 1.15)
    fps = VideoFileClip(video_path).fps

    # Calculate the total number of frames
    total_frames = int(end_time * fps)

    # Calculate the duration for which the transparency will change
    fade_duration = end_time / 5

    # Create ImageClips for each frame with gradually changing transparency
    overlay_clips = []
    fade_point = int(total_frames / 5 * 4)
    for frame_num in range(fade_point):
        frame_clip = overlay_image.set_duration(1 / fps).set_start(frame_num / fps).set_end((frame_num + 1) / fps)
        overlay_clips.append(frame_clip)

    for frame_num in range(fade_point, total_frames):
        transparency = 1.0 - min(1.0, (frame_num - fade_point) * (1.0 / (fade_duration * fps)))
        frame_clip = overlay_image.set_duration(1 / fps).set_start(frame_num / fps).set_end((frame_num + 1) / fps)
        frame_clip = frame_clip.set_opacity(transparency)
        overlay_clips.append(frame_clip)

    return overlay_clips

# def resize(t, duration):
#     if duration == 0:
#         return 1
#     # Starting scale factor
#     start_scale = 1
#     # End scale factor (the size to which the text should grow)
#     end_scale = 1.1
#     # Calculate the scaling factor based on elapsed time and total duration
#     scale_factor = start_scale + t/duration * (end_scale - start_scale)
#     return scale_factor
