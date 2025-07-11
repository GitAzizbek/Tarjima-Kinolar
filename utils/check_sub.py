import json
from aiogram import Bot
from database import *

PENDING_REQUESTS_PATH = "data/pending_requests.json"

def load_pending_requests():
    try:
        with open(PENDING_REQUESTS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

async def check_subscription(user_id: int, bot: Bot) -> bool:
    pending_requests = load_pending_requests()
    channels = load_channels()

    for ch in channels:
        ch_id = ch.get("chat_id")

        # ✅ 1. Private kanal uchun: -100 bilan boshlanadigan raqamli ID
        is_private = isinstance(ch_id, int) or (isinstance(ch_id, str) and ch_id.startswith("-100"))

        # 2. Pending request orqali tekshirish
        try:
            if any(
                str(req["user_id"]) == str(user_id) and str(req["chat_id"]) == str(ch_id)
                for req in pending_requests
            ):
                continue  # ✅ Obuna bo'lgan

            # 3. Realtime get_chat_member bilan tekshirish
            member = await bot.get_chat_member(chat_id=ch_id, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False

        except Exception as e:
            print(f"⚠️ Xatolik kanal bilan: {ch.get('title', ch_id)} — {e}")
            return False

    return True