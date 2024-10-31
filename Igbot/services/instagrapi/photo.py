from Igbot.helpers import get_photo_file, get_caption, delete_directory


def post_photo(cl, file_path, caption_text=None):
    photo_paths = get_photo_file(file_path)

    caption = ""
    if caption_text:
        caption = caption_text
    else:
        caption = get_caption(file_path)

    cl.album_upload(paths=photo_paths, caption=caption)

    delete_directory(file_path)
