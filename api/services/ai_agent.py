import asyncio
import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from loguru import logger
from openai import AsyncOpenAI

from app.memory import session_memory

load_dotenv()

# client_open = AsyncOpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=os.getenv("OPENAI_API_KEY")
# )
#
# async def chat_with_ai(user_id: str, user_message: str):
#     try:
#         messages = [{"role": "user", "content": user_message}]
#         response = await client_open.chat.completions.create(
#             model="deepseek/deepseek-chat-v3-0324:free",
#             messages=messages
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         print("Xatolik:", e)
#         return "Xatolik yuz berdi: " + str(e)
#
# #Deepsek yordamida https://openrouter.ai/keys ->link
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))



async def generate_reply_stream(
    user_id: str, user_message: str
) -> AsyncGenerator[str, None]:
    try:
        session_memory.add(user_id, "user", user_message)
        messages = session_memory.get(user_id)[-4:]

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.6,
            stream=True,
        )

        async for chunk in response:
            if chunk.choices[0].delta.content:
                content_piece = chunk.choices[0].delta.content
                yield content_piece
                await asyncio.sleep(0.05)

    except Exception as e:
        logger.info(f"{user_id} uchun yuborilayotgan messages: {messages}")
        yield f"❌ Xatolik yuz berdi: {str(e)}"