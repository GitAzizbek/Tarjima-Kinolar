from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNEL_USERNAME
from aiogram import Bot
from database import load_channels

async def subscribe_keyboard(user_id: int, bot: Bot):
    channels = load_channels()
    buttons = []
    index = 1  # Tartib raqami

    for ch in channels:
        try:
            member = await bot.get_chat_member(chat_id=ch["chat_id"], user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                btn_text = f"{index} - {ch['title']}"
                buttons.append([
                    InlineKeyboardButton(text=btn_text, url=ch["url"])
                ])
                index += 1
        except Exception as e:
            print(f"⚠️ Xatolik kanal bilan: {ch.get('title')} — {e}")
            continue

    # Tugma bo‘sh bo‘lsa ham "Obuna bo‘ldim" tugmasi qo‘shiladi
    buttons.append([
        InlineKeyboardButton(text="✅ Obuna bo‘ldim", callback_data="check_subs")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


