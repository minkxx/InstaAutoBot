from Igbot.helpers import get_reel_file, delete_directory, get_caption


def post_reel(cl, file_path, caption_text=None):
    reel_path = get_reel_file(file_path)

    caption = ""
    if caption_text:
        caption = caption_text
    else:
        caption = get_caption(file_path)

    cl.video_upload(path=reel_path, caption=caption)

    delete_directory(file_path)
