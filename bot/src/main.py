import asyncio
import logging
import tracemalloc

from aiogram import Bot, Dispatcher
from core import Config
from handlers.handlers import tg_router

bot = Bot(Config.BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(tg_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    tracemalloc.start()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')