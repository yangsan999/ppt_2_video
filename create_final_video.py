from subprocess import call


def create_final_video(video_list_str_path, output_video):
    print('Start combine final video, you are almost success')
    call(["ffmpeg",
          '-hide_banner',
          '-loglevel', 'error',
          '-y', '-f', 'concat',
         '-safe', '0', '-i', video_list_str_path, '-c', 'copy', output_video])
    print(str(output_video) + " is success")
