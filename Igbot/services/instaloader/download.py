import instaloader


def insta_download(short_code):
    loader = instaloader.Instaloader()

    try:
        post = instaloader.Post.from_shortcode(loader.context, short_code)
        loader.download_post(post, target=short_code)
        print(f"Reel and caption downloaded successfully to {short_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
