from aiogram import Router
from aiogram.types import ChatJoinRequest
from utils.join_db import add_join_request

router = Router()

@router.chat_join_request()
async def handle_join_request(event: ChatJoinRequest):
    user_id = event.from_user.id
    chat_id = event.chat.id
    add_join_request(user_id, chat_id)
