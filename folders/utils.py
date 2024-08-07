import os
import shutil


def create_or_clear_folder(folder_path):
    if not os.path.exists(folder_path):
        # create folder
        os.makedirs(folder_path)
    else:
        # clear folder contents
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isdir(file_path):
                # if is folder remove it recursively
                shutil.rmtree(file_path)
            else:
                # remove file
                os.remove(file_path)
