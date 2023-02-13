import asyncio
import os
from temp_dir import set_temp_dir, cleanup_temp_files
from create_images_audios import create_images_audios
from create_slide_videos import create_slide_videos
from create_final_video import create_final_video


def main():
    temp_path, image_folder = set_temp_dir()
    asyncio.run(create_images_audios(temp_path, image_folder, input_pptx))
    video_list_str_path = create_slide_videos(temp_path, image_folder)
    create_final_video(video_list_str_path, output_video)

    cleanup_temp_files(temp_path)
    print("clean up is success, you have done all job!")


if __name__ == '__main__':
    directory = os.path.join(os.getcwd(), 'input')
    filenames = os.listdir(directory)
    for filename in filenames:
        if filename.endswith(".pptx"):
            input_pptx = os.path.join(directory, filename)
            output_video = os.path.join(
                os.getcwd(), 'output', os.path.splitext(filename)[0] + ".mp4")
            main()
