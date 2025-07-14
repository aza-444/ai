import asyncio
import os

import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter
from aiogram.types import Message
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

logger.add("chat.log", rotation="1 day", retention="7 days", level="TRACE")

dp = Dispatcher()


async def start_hello(msg: Message, bot: Bot):
    await msg.answer(
        text=f"""
Assalomu alaykum, <b>{msg.from_user.first_name}</b>! 😊
O'zimni tanishtirishga ijozat bering:
• Men sizning <b>topshiriq va savollaringizda</b> yordam berish uchun yaratilgan sun'iy idrokman 🤖
• <b>Matn</b> bilan bog'liq har qanday topshiriqni bajara olaman 📝
• <b>Rasmlar</b>-chi deysizmi? Ularni ham tushunaman, ham yuklab beraman 🔎
• <b>Google</b>dan sizga kerak bo'lgan sahifalarni ham topib bera olaman 🌐
• Quyida chap burchakda ko'k rangdagi menyu tugmachasi bor, shu orqali men haqimda batafsilroq bilib olishingiz mumkin 😉""",
        parse_mode="html",
    )


async def on_startup(bot: Bot):
    await bot.send_message(chat_id=os.getenv("USER_ID"), text="Bot Ishga tushdi ✅")


async def on_shutdown(bot: Bot):
    await bot.send_message(chat_id=os.getenv("USER_ID"), text="Bot To'xtadi ⚠️")
    await bot.session.close()


async def handle_message(message: types.Message):
    logger.info(f"{message.from_user.id} -> {message.text}")
    user_id = str(message.from_user.id)

    allowed_users = os.getenv("ALLOWED_USERS", "")
    if user_id not in allowed_users:
        await message.reply("🚫 Sizga ruxsat yo‘q.")
        return

    sent = await message.answer("🔄 Javob yozilmoqda...")

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                    "POST",
                    os.getenv("API_URL"),
                    json={"user_id": user_id, "message": message.text},
            ) as response:

                if response.status_code == 200:
                    partial_text = ""
                    async for line in response.aiter_lines():
                        if not line.strip():
                            continue
                        partial_text += line + " "

                        try:
                            await message.bot.edit_message_text(
                                chat_id=sent.chat.id,
                                message_id=sent.message_id,
                                text=partial_text.strip(),
                                parse_mode=ParseMode.MARKDOWN,
                            )
                            await asyncio.sleep(1)
                        except TelegramRetryAfter as e:
                            await asyncio.sleep(e.retry_after)
                        except TelegramBadRequest:
                            continue

                elif response.status_code == 401:
                    error_text = "❌ API token noto‘g‘ri yoki mavjud emas. Admin bilan bog‘laning."
                    await message.bot.edit_message_text(
                        chat_id=sent.chat.id,
                        message_id=sent.message_id,
                        text=error_text,
                        parse_mode=ParseMode.MARKDOWN,
                    )

                elif response.status_code == 429:
                    error_text = (
                        "🚫 Limit tugagan. Iltimos, kuting yoki kredit to‘ldiring."
                    )
                    await message.bot.edit_message_text(
                        chat_id=sent.chat.id,
                        message_id=sent.message_id,
                        text=error_text,
                        parse_mode=ParseMode.MARKDOWN,
                    )


                else:
                    error_text = f"⚠️ Server xatoligi: {response.status_code}"
                    await message.bot.edit_message_text(
                        chat_id=sent.chat.id,
                        message_id=sent.message_id,
                        text=error_text,
                        parse_mode=ParseMode.MARKDOWN,
                    )

    except httpx.HTTPError as e:
        error_text = f"❌ HTTP xatosi: {e}"
        await message.bot.edit_message_text(
            chat_id=sent.chat.id,
            message_id=sent.message_id,
            text=error_text,
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as e:
        error_text = f"❌ Noma’lum xatolik: {e}"
        await message.bot.edit_message_text(
            chat_id=sent.chat.id,
            message_id=sent.message_id,
            text=error_text,
            parse_mode=ParseMode.MARKDOWN,
        )
