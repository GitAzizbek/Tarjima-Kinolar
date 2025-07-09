from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNEL_USERNAME
from database import load_channels

async def subscribe_keyboard(user_id, bot):
    channels = load_channels()
    buttons = []

    index = 1  # tartib raqami uchun

    for ch in channels:
        try:
            member = await bot.get_chat_member(chat_id=ch, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                # Faqat obuna bo‘lmaganlarni raqam bilan tugmaga qo‘shamiz
                btn_text = f"{index} - kanal"
                buttons.append([InlineKeyboardButton(text=btn_text, url=f"https://t.me/{ch.lstrip('@')}")])
                index += 1
        except Exception:
            continue

    buttons.append([InlineKeyboardButton(text="✅ Obuna bo‘ldim", callback_data="check_subs")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


