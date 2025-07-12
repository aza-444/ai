import asyncio
import os

import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter
from aiogram.types import Message
from dotenv import load_dotenv
from loguru import logger

load_dotenv()
dp = Dispatcher()


async def start_hello(msg: Message, bot: Bot):
    await msg.answer(
        text=f"""
Assalomu alaykum,<b>{msg.from_user.first_name}</b>! 😊
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


logger.add("chat.log", rotation="1 day", retention="7 days", level="TRACE")

async def handle_message(message: types.Message):
    logger.info(f"{message.from_user.id} -> {message.text}")
    user_id = str(message.from_user.id)
    allowed_users = os.getenv("ALLOWED_USERS")

    if user_id not in allowed_users:
        await message.reply("🚫 Sizga ruxsat yo‘q.")
        return

    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    sent = await message.answer("🔄 Javob yozilmoqda...")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                os.getenv("API_URL"),
                json={"user_id": user_id, "message": message.text}
            )

        if response.status_code == 200:
            try:
                data = response.json()
                full_reply = data.get("reply") or "⚠️ Javob mavjud emas."
            except ValueError:
                full_reply = "❗️ Server noto‘g‘ri formatda javob qaytardi."
        elif response.status_code == 401:
            full_reply = "❌ API token noto‘g‘ri yoki mavjud emas. Admin bilan bog‘laning."
        elif response.status_code == 429:
            full_reply = "🚫 Foydalanish limiti tugagan. Iltimos, biroz kutib qayta urinib ko‘ring yoki kredit to‘ldiring."
        else:
            full_reply = f"⚠️ Server xatoligi: {response.status_code}"

    except httpx.HTTPError as e:
        full_reply = f"❌ So‘rov vaqtida xatolik yuz berdi: {e}"
    except Exception as e:
        full_reply = f"❌ Noma’lum xatolik: {e}"

    if "\n" in full_reply or len(full_reply.split()) > 200:
        try:
            await message.bot.edit_message_text(
                chat_id=sent.chat.id,
                message_id=sent.message_id,
                text=full_reply,
                parse_mode="Markdown"
            )
        except (TelegramRetryAfter, TelegramBadRequest):
            pass
        return

    sozlar = full_reply.split()
    soz_uzunligi = 10
    oxirgi_soz = ""
    chashka = []

    for i, word in enumerate(sozlar, start=1):
        chashka.append(word)
        if i % soz_uzunligi == 0 or i == len(sozlar):
            candidate = " ".join(chashka)
            if candidate != oxirgi_soz:
                oxirgi_soz += candidate
                try:
                    await asyncio.sleep(0.5)
                    await message.bot.edit_message_text(
                        chat_id=sent.chat.id,
                        message_id=sent.message_id,
                        text=oxirgi_soz,
                        parse_mode="Markdown"
                    )
                except TelegramRetryAfter as e:
                    await asyncio.sleep(e.retry_after)
                    await message.bot.edit_message_text(
                        chat_id=sent.chat.id,
                        message_id=sent.message_id,
                        text=oxirgi_soz,
                        parse_mode="Markdown"
                    )
                except TelegramBadRequest:
                    pass
            chashka = []

    if oxirgi_soz != full_reply:
        try:
            await asyncio.sleep(0.5)
            await message.bot.edit_message_text(
                chat_id=sent.chat.id,
                message_id=sent.message_id,
                text=full_reply,
                parse_mode="Markdown"
            )
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            await message.bot.edit_message_text(
                chat_id=sent.chat.id,
                message_id=sent.message_id,
                text=full_reply,
                parse_mode="Markdown"
            )
        except TelegramBadRequest:
            pass
