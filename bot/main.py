import asyncio
import logging
import os
import sys

import httpx
from aiogram import Bot, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.dispatcher import dp, on_startup, on_shutdown, handle_message
from utils.utils import Config


async def main(bot: Bot) -> None:
    dp.message()(handle_message)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=Config.bot.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    asyncio.run(main(bot))
