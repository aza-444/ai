import os

import httpx
from aiogram import Dispatcher, Bot, types
from aiogram.types import Message

dp = Dispatcher()


async def on_startup(bot: Bot):
    await bot.send_message(chat_id=os.getenv("USER_ID"), text="Bot Ishga tushdi ✅")


async def on_shutdown(bot: Bot):
    await bot.send_message(chat_id=os.getenv("USER_ID"), text="Bot To'xtadi ⚠️")
    await bot.session.close()

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