import asyncio
import logging
import tracemalloc

from aiogram import Bot, Dispatcher
from core import Config, container
from handlers.handlers import tg_router
from utils.daily_bet_creator import daily_bet_creator

bot = Bot(Config.BOT_TOKEN)
dp = Dispatcher()

async def on_startup(bot: Bot):
    asyncio.create_task(daily_bet_creator(container.SessionLocal))

async def main():
    dp.include_router(tg_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    tracemalloc.start()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')