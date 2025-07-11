from aiogram import Router, types
from database import add_pending_request

router = Router()

@router.chat_join_request()
async def handle_join_request(event: types.ChatJoinRequest):
    add_pending_request(user_id=event.from_user.id, chat_id=event.chat.id)
    try:
        await event.answer(approved=False)  # Yoki False — faqat so'rov yuborish uchun
    except Exception as e:
        print(f"❌ Join requestda xatolik: {e}")