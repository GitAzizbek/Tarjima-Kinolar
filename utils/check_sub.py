from aiogram import Bot

from config import CHANNEL_USERNAME
from database import load_channels
from utils.join_db import has_join_request
from database import *
from aiogram.exceptions import TelegramBadRequest

async def check_subscription(user_id: int, bot: Bot) -> bool:
    channels = load_channels()
    for ch in channels:
        chat_id = ch.get("chat_id")
        try:
            # 1️⃣ Avval "pending" so‘rovlar orasida bormi tekshir
            if is_user_pending(user_id, chat_id):
                continue  # Bu kanal bo‘yicha obuna deb hisoblaymiz

            # 2️⃣ Aks holda oddiy get_chat_member bilan tekshir
            member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception:
            return False
    return True