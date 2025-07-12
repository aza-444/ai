import asyncio
import logging
import sys

from aiogram import Bot, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from bot.dispatcher import dp, handle_message, on_shutdown, on_startup, start_hello
from utils.utils import Config


async def main(bot: Bot) -> None:
    dp.message.register(start_hello, CommandStart())
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.message()(handle_message)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(
        token=Config.bot.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    asyncio.run(main(bot))
