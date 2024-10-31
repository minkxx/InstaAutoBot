from pyrogram import filters, Client
from pyrogram.types import Message

from Igbot import bot


@bot.on_message(filters.command("start"))
async def start(c: bot, m: Message):
    await c.send_message(chat_id=m.chat.id, text="Started!", reply_to_message_id=m.id)
