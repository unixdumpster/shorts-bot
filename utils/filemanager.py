import os
import utils.generate_videos as gv


def initialize_directories():
    """
    :return: triple
        raw_video_dir: str
        raw_audio_dir: str
        finalized_products_dir: str
    """

    raw_video_dir = create_directory('raw_videos')
    raw_audio_dir = create_directory('raw_audios')
    final_product_dir = create_directory('final_products')

    if len(os.listdir(str(raw_video_dir))) == 0:
        gv.generate_videos(raw_video_dir)

    return raw_video_dir, raw_audio_dir, final_product_dir


def create_directory(directory):
    dir_name = os.path.join(os.getcwd(), directory)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    return dir_name


def cleanup_directory(directory):
    files = os.listdir(directory)

    for file_name in files:
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    try:
        os.rmdir(directory)
    except OSError as error:
        print(error)