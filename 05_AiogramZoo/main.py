import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from router import router, db, DEBUG
from config import TELEGRAM_TOKEN


async def main() -> None:
    """ Startup function """
    await db.initialize_database()

    bot = Bot(TELEGRAM_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)  # Удаляет накопленые входящие
    await dp.start_polling(bot)


if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
