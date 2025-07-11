from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot
from database import *
from utils.check_sub import load_pending_requests

async def subscribe_keyboard(user_id: int, bot: Bot):
    channels = load_channels()
    pending_requests = load_pending_requests()  # [{"user_id": 123, "channel_id": -10012345}, ...]
    buttons = []
    index = 1

    for ch in channels:
        chat_id = ch["chat_id"]
        url = ch["url"]
        title = ch.get("title", f"{index} - kanal")

        # ✅ Avval `pending_requests.json` ichidan tekshiramiz
        joined = any(
            str(req["user_id"]) == str(user_id) and str(req["chat_id"]) == str(chat_id)
            for req in pending_requests
        )

        if joined:
            continue  # allaqachon join request yuborgan

        try:
            # get_chat_member bilan tekshirish
            member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            if member.status in ["member", "administrator", "creator"]:
                continue  # allaqachon obuna bo‘lgan
        except Exception as e:
            print(f"⚠️ Xatolik kanal bilan: {title} — {e}")
            # Xatolik bo‘lsa ham davom etamiz

        # Obuna bo‘lmaganlar uchun tugma
        btn_text = f"{index} - {title}"
        buttons.append([
            InlineKeyboardButton(text=btn_text, url=url)
        ])
        index += 1

    buttons.append([
        InlineKeyboardButton(text="✅ Obuna bo‘ldim", callback_data="check_subs")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)