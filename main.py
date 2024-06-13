from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
import asyncio

from bot.handlers import router


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot offline')
