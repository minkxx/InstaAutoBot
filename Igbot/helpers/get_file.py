import os


def get_reel_file(file_path):
    for file in os.listdir(file_path):
        if file.endswith(".mp4"):
            return os.path.join(file_path, file)


def get_photo_file(file_path):
    files = []
    for file in os.listdir(file_path):
        if file.endswith(".jpg") or file.endswith(".png"):
            files.append(os.path.join(file_path, file))
    return files


def get_caption(file_path):
    for file in os.listdir(file_path):
        if file.endswith(".txt"):
            with open(os.path.join(file_path, file), "r", encoding="utf-8") as f:
                caption = f.read()
            return caption
