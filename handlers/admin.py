from aiogram import Router, types, F
from aiogram.filters import Command
from config import ADMIN_IDS, MOVIE_JSON_PATH, CHANNEL_USERNAME
from keyboards.default import admin_menu
from database import *
from utils.misc import get_username
from aiogram.fsm.context import FSMContext
from states.admin_states import UploadMovie
from database import get_movie_by_code


import os

router = Router()

from database import get_user_count

@router.message(Command("addchannel"))
async def add_new_channel(message: types.Message):
    if not is_admin(message):
        return await message.answer("⛔ Siz admin emassiz!")

    parts = message.text.strip().split(maxsplit=4)
    if len(parts) != 5:
        return await message.answer(
            "❗ Foydalanish:\n"
            "<code>/addchannel type chat_id url title</code>\n\n"
            "Masalan:\n"
            "<code>/addchannel public @kanalim https://t.me/kanalim Kanal nomi</code>\n"
            "<code>/addchannel private -1001234567890 https://t.me/+abc123 Yopiq kanal</code>",
            parse_mode="HTML"
        )

    ch_type, chat_id, url, title = parts[1], parts[2], parts[3], parts[4]

    if ch_type not in ["public", "private"]:
        return await message.answer("❌ Kanal turi noto‘g‘ri: 'public' yoki 'private' bo‘lishi kerak.")

    success = add_channel({
        "type": ch_type,
        "chat_id": chat_id,
        "url": url,
        "title": title
    })

    if success:
        return await message.answer(f"✅ Kanal qo‘shildi:\n<b>{title}</b>\n🔗 {url}", parse_mode="HTML")
    else:
        return await message.answer("⚠️ Bu kanal allaqachon mavjud yoki xatolik yuz berdi.")

@router.message(Command("removechannel"))
async def remove_channel_cmd(message: types.Message):
    if not is_admin(message):
        return await message.answer("⛔ Siz admin emassiz!")

    parts = message.text.strip().split()
    if len(parts) != 2:
        return await message.answer("❗ Foydalanish: /removechannel chat_id")

    chat_id = parts[1]
    removed = remove_channel(chat_id)

    if removed:
        await message.answer(f"🗑 Kanal o‘chirildi: <code>{chat_id}</code>", parse_mode="HTML")
    else:
        await message.answer("❌ Kanal topilmadi yoki allaqachon o‘chirilgan.")

@router.message(Command("channels"))
async def list_channels(message: types.Message):
    if not is_admin(message):
        return await message.answer("⛔ Siz admin emassiz!")

    channels = load_channels()
    if not channels:
        return await message.answer("📭 Hozircha hech qanday kanal mavjud emas.")

    text = "📢 Obuna talab qilinadigan kanallar:\n\n"
    for idx, ch in enumerate(channels, start=1):
        text += f"{idx}. {ch['title']} — <code>{ch['chat_id']}</code>\n"

    await message.answer(text, parse_mode="HTML")


def save_movie(code, data):
    code = code.upper()
    movies = load_movies()
    movies[code] = data

    backup_movies()

    with open(MOVIE_JSON_PATH, "w") as f:
        json.dump(movies, f, indent=4)


@router.message(F.text == "📊 Statistika")
@router.message(Command("stats"))
async def show_stats(message: types.Message):
    if not is_admin(message):
        return await message.answer("⛔ Siz admin emassiz!")

    users = load_users()
    user_count = len(users)

    text = f"📈 Umumiy foydalanuvchilar: <b>{user_count}</b>\n\n"

    for user in users[:20]:  # faqat dastlabki 20 ta foydalanuvchi
        name = f"{user['first_name']} {user.get('last_name', '')}".strip()
        uname = f"@{user['username']}" if user['username'] else ""
        text += f"• {name} {uname}\n"

    await message.answer(text)


def is_admin(message: types.Message) -> bool:
    return message.from_user.id in ADMIN_IDS

@router.message(Command("admin"))
async def admin_start(message: types.Message):
    if not is_admin(message):
        return await message.answer("⛔ Siz admin emassiz!")
    await message.answer("📥 Admin paneliga xush kelibsiz!", reply_markup=admin_menu)

@router.message(F.text == "📤 Kino yuklash")
async def ask_to_send_video(message: types.Message):
    if not is_admin(message):
        return await message.answer("⛔ Siz admin emassiz!")
    await message.answer("🎞 Iltimos, kino videosini yuboring.")

@router.message(F.video)
async def handle_video_upload(message: types.Message, state: FSMContext):
    if not is_admin(message):
        return await message.answer("⛔ Siz admin emassiz!")

    await state.set_data({"file_id": message.video.file_id})
    await state.set_state(UploadMovie.waiting_for_code)
    await message.answer("✅ Video qabul qilindi.\nIltimos, kino kodi yuboring:")

@router.message(UploadMovie.waiting_for_code)
async def process_code(message: types.Message, state: FSMContext):
    if not is_admin(message):
        return await message.answer("⛔ Siz admin emassiz!")

    code = message.text.strip().upper()

    if get_movie_by_code(code):
        return await message.answer("❗️ Bu kod allaqachon mavjud! Iltimos, boshqa kod kiriting.")

    await state.update_data({"code": code})
    await state.set_state(UploadMovie.waiting_for_description)
    await message.answer("📝 Endi kino tavsifini (description) yuboring:")

@router.message(UploadMovie.waiting_for_description)
async def process_description(message: types.Message, state: FSMContext):
    if not is_admin(message):
        return await message.answer("⛔ Siz admin emassiz!")

    desc = message.text.strip()
    data = await state.get_data()
    file_id = data["file_id"]
    code = data["code"]

    movie_data = {
        "title": f"Kod: {code}",
        "description": desc,
        "file_id": file_id,
        "type": "video"
    }

    save_movie(code, movie_data)
    await message.answer(f"✅ Kino saqlandi!\n🎞 Kod: {code}\n📝 Tavsif: {desc}")

    try:
        await message.bot.send_video(
            chat_id=CHANNEL_USERNAME,
            video=file_id,
            caption=f"🎬 Kino kodi: <code>{code}</code>\n📝 {desc}"
        )
    except Exception as e:
        await message.answer(f"⚠️ Kanalga yuborilmadi: {e}")

    await state.clear()


