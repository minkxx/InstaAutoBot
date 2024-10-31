from pyrogram import filters, Client, enums
from pyrogram.types import Message, InputMediaPhoto, CallbackQuery

from Igbot import bot
from Igbot.services.instaloader import insta_download
from Igbot.services.instagrapi import load_client, post_photo, post_reel
from Igbot.helpers import get_photo_file, get_reel_file, get_caption, delete_directory
from Igbot.helpers.keyboards import ikb
from Igbot.database import db_get_ig_acc


@bot.on_message(
    filters.regex(
        pattern=r"https:\/\/www\.instagram\.com\/(reel|p)\/[A-Za-z0-9_-]+\/\?igsh=[A-Za-z0-9=_-]+"
    )
)
async def insta(c: Client, m: Message):
    url = m.text
    short_code = url.split("/")[-2]
    i_type = url.split("/")[-3]

    acc_data = db_get_ig_acc(user_id=m.chat.id)

    insta_download(short_code)

    if not acc_data:
        if i_type == "reel":
            reel_path = get_reel_file(short_code)
            caption = get_caption(short_code)
            await c.send_chat_action(chat_id=m.chat.id, action=enums.ChatAction.UPLOAD_VIDEO)
            await c.send_video(chat_id=m.chat.id, video=reel_path, caption=caption)

        elif i_type == "p":
            photo_paths = get_photo_file(short_code)

            if len(photo_paths) == 1:
                await c.send_chat_action(chat_id=m.chat.id, action=enums.ChatAction.UPLOAD_PHOTO)
                await c.send_photo(
                    chat_id=m.chat.id, photo=photo_paths[0], caption=caption
                )
            else:
                await c.send_chat_action(chat_id=m.chat.id, action=enums.ChatAction.UPLOAD_PHOTO)
                await c.send_media_group(
                    chat_id=m.chat.id,
                    media=[
                        InputMediaPhoto(media=i, caption=caption) for i in photo_paths
                    ],
                )

        delete_directory(short_code)
    else:
        key_data = {}
        for user in acc_data:
            key_data[user] = f"dl={user}={i_type}={short_code}"

        keyboard = ikb(key_data)

        if i_type == "reel":
            reel_path = get_reel_file(short_code)
            caption = get_caption(short_code)
            await c.send_chat_action(chat_id=m.chat.id, action=enums.ChatAction.UPLOAD_VIDEO)
            await c.send_video(
                chat_id=m.chat.id,
                video=reel_path,
                caption=caption,
                reply_markup=keyboard,
            )

        elif i_type == "p":
            photo_paths = get_photo_file(short_code)

            if len(photo_paths) == 1:
                await c.send_chat_action(chat_id=m.chat.id, action=enums.ChatAction.UPLOAD_PHOTO)
                await c.send_photo(
                    chat_id=m.chat.id,
                    photo=photo_paths[0],
                    caption=caption,
                    reply_markup=keyboard,
                )
            else:
                username = await c.ask(
                    chat_id=m.chat.id,
                    text="Can't send upload keyboard with multiple medias.\n\nEnter account name manually to upload it.\n\n/cancel - to cancel upload",
                )
                if username.text != "/cancel":
                    password = acc_data[username.text]
                    ig_cli = load_client(c, m.chat.id, username.text, password)
                    cap = c.ask(
                        chat_id=m.chat.id,
                        text="Enter caption (1 to set default caption)",
                    )
                    if cap.text == "1":
                        post_photo(ig_cli, photo_paths)
                    else:
                        post_photo(ig_cli, photo_paths, cap.text)

                    await c.send_message(chat_id=m.chat.id, text=f"Uploaded photo album to account: `{username}`")

                else:
                    return


@bot.on_callback_query(filters.regex(pattern="^(dl=.*=.*=.*)$"))
async def upload(c: Client, cbq: CallbackQuery):
    user_id = cbq.message.chat.id
    d = cbq.data.split("=")
    username = d[1]
    i_type = d[2]
    short_code = d[3]

    acc_data = db_get_ig_acc(user_id)
    password = acc_data[username]

    ig_cli = load_client(c, user_id, username, password)

    if i_type == "reel":
        reel_path = get_reel_file(short_code)
        cap = c.ask(chat_id=user_id, text="Enter caption (1 to set default caption)")
        if cap.text == "1":
            post_reel(ig_cli, reel_path)
        else:
            post_reel(ig_cli, reel_path, cap.text)

        await c.send_message(chat_id=user_id, text=f"Uploaded reel to account: `{username}`")
    elif i_type == "p":
        photo_paths = get_photo_file(short_code)
        cap = c.ask(chat_id=user_id, text="Enter caption (1 to set default caption)")
        if cap.text == "1":
            post_photo(ig_cli, photo_paths)
        else:
            post_photo(ig_cli, photo_paths, cap.text)

        await c.send_message(chat_id=user_id, text=f"Uploaded photo to account: `{username}`")
