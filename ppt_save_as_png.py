import os
from pptx_tools import utils  # pip install python-pptx-interface

def ppt_save_as_png(image_folder, input_pptx):

    if utils.save_pptx_as_png(image_folder, input_pptx, overwrite_folder=True):
        print("ppt save as png is success")
    else:
        raise SystemExit

    # Iterate over the files in the directory
    for file in os.listdir(image_folder):
        # Get the file name and extension
        name, ext = os.path.splitext(file)

        # Extract the number from the file name, number -1 to make start with 0
        num = str(int(name.split('幻灯片')[1])-1)

        # Rename the file using the new naming convention
        os.rename(os.path.join(image_folder, file), os.path.join(
            image_folder, 'slide_{}{}'.format(num, ext)))

    print("png rename is success")
