from aiogram import Router, types, F
from aiogram.filters import CommandStart
from keyboards.default import user_menu
from utils.check_sub import check_subscription
from config import CHANNEL_USERNAME
from database import get_movie_by_code
from keyboards.inline import subscribe_keyboard
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    if not await check_subscription(message.from_user.id, message.bot):
        kb = await subscribe_keyboard(message.from_user.id, message.bot)
        return await message.answer("👋 Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:", reply_markup=kb)

    await message.answer("🎬 Kino kodini yuboring:")



@router.callback_query(F.data == "check_subs")
async def recheck_subscription(callback: CallbackQuery):
    is_subscribed = await check_subscription(callback.from_user.id, callback.bot)

    if is_subscribed:
        try:
            await callback.message.edit_text("✅ Obuna tasdiqlandi! Endi kino kodini yuboring.")
        except TelegramBadRequest as e:
            if "message is not modified" not in str(e):
                raise e
    else:
        keyboard = await subscribe_keyboard(callback.from_user.id, callback.bot)
        try:
            await callback.message.edit_text(
                "❌ Hali ham barcha kanallarga obuna bo‘lmagansiz.\nIltimos, quyidagilarga obuna bo‘ling:",
                reply_markup=keyboard
            )
        except TelegramBadRequest as e:
            if "message is not modified" not in str(e):
                raise e



@router.message(F.text == "🎬 Kino kodi yuborish")
async def handle_button_press(message: types.Message):
    await message.answer("📥 Kino kodini yuboring:")



@router.message(F.text)
async def handle_movie_code(message: types.Message):
    if not await check_subscription(message.from_user.id, message.bot):
        await message.answer(
            "⛔ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling.",
            reply_markup= await subscribe_keyboard(message.from_user.id, message.bot)
        )
        return


    code = message.text.strip().upper()
    movie = get_movie_by_code(code)

    if movie:
        await message.bot.send_video(message.chat.id, video=movie["file_id"], caption=f"🎬 <b>{movie['title']}</b>\n📝 {movie['description']}")
    else:
        await message.answer("❌ Bunday kino kodi topilmadi.")
