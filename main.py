from aiogram import Bot, Dispatcher
import asyncio

from config import settings
from bot.handlers import router
from aiogram.fsm.storage.redis import RedisStorage

storage = RedisStorage.from_url(f"redis://{settings.redis_username}:{settings.redis_pass}@{settings.redis_host}:{settings.redis_port}/{settings.redis_db}")


async def main():
    bot = Bot(token=settings.telegram_token)
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot offline')
