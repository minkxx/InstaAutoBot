from pyrogram import Client, filters
from pyrogram.types import Message

from Igbot import bot
from Igbot.database import db_add_ig_acc, db_get_ig_acc, db_rm_ig_acc


@bot.on_message(filters.command("add_acc"))
async def add_account(c: Client, m: Message):
    username = await c.ask(chat_id=m.chat.id, text="Enter your Instagram username")
    password = await c.ask(chat_id=m.chat.id, text="Enter your Instagram password")
    db_add_ig_acc(m.chat.id, username.text, password.text)
    await c.send_message(chat_id=m.chat.id, text=f"Done! added {username.text}")


@bot.on_message(filters.command("del_acc"))
async def add_account(c: Client, m: Message):
    username = await c.ask(chat_id=m.chat.id, text="Enter your Instagram username")
    db_rm_ig_acc(m.chat.id, username.text)
    await c.send_message(chat_id=m.chat.id, text=f"Done! deleted {username.text}")


@bot.on_message(filters.command("get_accs"))
async def add_account(c: Client, m: Message):
    data = db_get_ig_acc(m.chat.id)
    if data:
        text = "Here are your accs (user:pass)\n\n"
        for username in data:
            text += f"`{username}` : `{data[username]}`"
        await c.send_message(chat_id=m.chat.id, text=text, reply_to_message_id=m.id)
    else:
        await c.send_message(
            chat_id=m.chat.id,
            text="You got no accounts added yet!",
            reply_to_message_id=m.id,
        )
