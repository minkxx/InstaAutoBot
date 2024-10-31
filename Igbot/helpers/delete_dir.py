import os
import shutil


def delete_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        print(f"Directory '{directory_path}' and all its contents have been deleted.")
    else:
        print(f"Directory '{directory_path}' does not exist.")
