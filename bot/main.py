import asyncio
import logging
import os
import sys

import httpx
from aiogram import Bot, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.dispatcher import dp, on_startup, on_shutdown
from utils.utils import Config


@dp.message()
async def handle_message(message: types.Message):
    user_id = str(message.from_user.id)
    allowed_users = os.getenv("USER_ID", "").split(",")

    if user_id not in allowed_users:
        await message.reply("Sizga ruxsat yo‘q.")
        return

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/chat",
                json={"user_id": user_id, "message": message.text},
                timeout=60
            )
            if response.status_code == 200:
                data =  response.json()
                reply = data.get("response", "Bo‘sh javob.")
            else:
                reply = f"Server xatoligi: {response.status_code}"
    except httpx.ReadTimeout:
        reply = "⏱ Server javob bermadi (timeout). Iltimos, qaytadan urinib ko‘ring."
    except Exception as e:
        reply = f"Xatolik yuz berdi:\n<code>{str(e)}</code>"

    await message.reply(reply, parse_mode="Markdown")



async def main(bot: Bot) -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=Config.bot.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    asyncio.run(main(bot))
