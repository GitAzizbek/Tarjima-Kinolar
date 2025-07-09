from aiogram import Bot

from config import CHANNEL_USERNAME


from database import load_channels
from aiogram.exceptions import TelegramBadRequest

async def check_subscription(user_id, bot):
    channels = load_channels()
    for channel in channels:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception:
            continue
    return True
