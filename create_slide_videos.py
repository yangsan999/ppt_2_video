import os
from subprocess import call


def create_slide_videos(temp_path, image_folder):
    num_videos = sum([len(files)
                     for root, dirs, files in os.walk(image_folder)])
    # Combine each slide image and audio into a video
    print('Start combine images and audios into videos, you may need to wait long, long, long time')
    for i in range(num_videos):
        image_path = os.path.join(image_folder, 'slide_{}.png'.format(i))
        audio_path = os.path.join(temp_path, 'slide_{}.mp3'.format(i))
        video_path = os.path.join(temp_path, 'slide_{}.mp4'.format(i))

        call(["ffmpeg",
              '-hide_banner',
              '-loglevel', 'error',
              '-y',
              '-loop', '1',  '-i', image_path,
              '-i', audio_path,
              '-c:v', 'libx264', '-b:v', '2400k',
              '-tune', 'stillimage', '-s', '1920x1080',
             '-c:a', 'aac', '-b:a', '320k',
              '-pix_fmt', 'yuv420p', '-shortest', '-r', '30',
              '-threads', '4', '-movflags', '+faststart', video_path])

        print(str('slide_{}.mp4'.format(i)) + " is success")

    video_list = [os.path.join(temp_path, 'slide_{}.mp4'.format(i))
                  for i in range(num_videos)]
    video_list_str = "\n".join(["file '{}'".format(f) for f in video_list])
    video_list_str_path = os.path.join(temp_path, 'video_list_str.txt')

    with open(video_list_str_path, 'w') as f:
        # Write the 'file' prefix and the file name to the file, one per line
        f.write(video_list_str)
        print("video_list_str.txt write is success")

    return (video_list_str_path)
