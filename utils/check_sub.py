from aiogram import Bot

from config import CHANNEL_USERNAME
from database import load_channels
from utils.join_db import has_join_request
from database import load_channels
from aiogram.exceptions import TelegramBadRequest

async def check_subscription(user_id: int, bot: Bot) -> bool:
    channels = load_channels()

    for ch in channels:
        chat_id = ch["chat_id"]

        if has_join_request(user_id, chat_id):
            continue  # join request bazada mavjud — o'tkazamiz

        try:
            member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception as e:
            print(f"Xatolik: {e}")
            return False

    return True

async def check_subscription(user_id: int, bot: Bot) -> bool:
    channels = load_channels()

    for ch in channels:
        try:
            member = await bot.get_chat_member(chat_id=ch["chat_id"], user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception as e:
            print(f"⚠️ Kanalga aʼzo tekshiruvda xatolik: {ch.get('title')} — {e}")
            return False  # Hatolik bo‘lsa ham foydalanuvchini o'tkazmaymiz

    return True  # Hammasiga obuna bo‘lsa