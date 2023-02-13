import shutil
import os
import tempfile


def set_temp_dir():
    temp_path = tempfile.mkdtemp()
    image_folder = os.path.join(temp_path, "images")
    os.makedirs(image_folder, exist_ok=True)
    return temp_path, image_folder


def cleanup_temp_files(temp_path):
    shutil.rmtree(temp_path)
