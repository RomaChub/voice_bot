from aiogram import Bot, Dispatcher
import asyncio

from config import settings, storage
from bot.handlers import router


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
