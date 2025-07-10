from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)


async def chat_with_ai(user_id: str, user_message: str):
    try:
        messages = [{"role": "user", "content": user_message}]
        response = await client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Xatolik:", e)
        return "Xatolik yuz berdi: " + str(e)
