import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from bot_config import API_TOKEN
from database import init_db
from handlers import start, profile, edit, teacher_pm, reply, admin_poll
from middlewares.rate_limit import RateLimitMiddleware


bot = Bot(API_TOKEN)
dp = Dispatcher()


async def set_commands():
    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск"),
        BotCommand(command="profile", description="Профіль"),
        BotCommand(command="send_poll", description="Опитування"),
        BotCommand(command="poll_results", description="Результати"),
        BotCommand(command="play", description="Грати")
    ])


async def main():
    await init_db()
    await set_commands()

    dp.include_routers(
        start.router,
        profile.router,
        edit.router,
        teacher_pm.router,
        reply.router,
        admin_poll.router
    )

    dp.message.middleware(RateLimitMiddleware())
    dp.callback_query.middleware(RateLimitMiddleware())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
