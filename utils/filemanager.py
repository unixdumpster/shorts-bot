import os
import utils.generate_videos as gv


def setup():
    """
    :return: triple
        raw_video_dir: str
        raw_audio_dir: str
        finalized_products_dir: str
    """
    if os.path.exists("screenshot.png"):
        os.remove("screenshot.png")

    raw_video_dir = os.path.join(os.getcwd(), 'raw_videos')
    raw_audio_dir = create_directory('raw_audios')
    final_product_dir = create_directory('final_products')

    if len(os.listdir(str(raw_video_dir))) < 3:
        cleanup_directory(raw_video_dir)
        create_directory('raw_videos')
        gv.generate_videos(raw_video_dir)

    return raw_video_dir, raw_audio_dir, final_product_dir


def teardown(raw_audio_dir, final_product_dir):
    cleanup_directory(raw_audio_dir)
    cleanup_directory(final_product_dir)
    os.remove("screenshot.png")


def create_directory(directory):
    dir_path = os.path.join(os.getcwd(), directory)

    # teardown failed in a previous run
    if os.path.exists(dir_path):
        cleanup_directory(dir_path)

    os.mkdir(dir_path)
    return dir_path


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
