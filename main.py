import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import user, admin
from handlers import join
from middlewares.register_user import RegisterUserMiddleware
from handlers import join_request

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    # Middleware
    dp.message.middleware(RegisterUserMiddleware())

    # Routerlar
    dp.include_router(join_request.router)
    dp.include_router(join.router)
    dp.include_router(admin.router)
    dp.include_router(user.router)
    

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
