from fastapi import FastAPI, Request
from pydantic import BaseModel

from api.services.ai_agent import chat_with_ai, chat_with_ai_async
from app.memory import session_memory

app = FastAPI()


class MessageIn(BaseModel):
    user_id: str
    message: str


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message")
    user_id = data.get("user_id")
    response = await chat_with_ai_async(user_id, message)
    return {"reply": response}


@app.post("/reset")
def reset(msg: MessageIn):
    session_memory.clear(msg.user_id)
    return {"status": "cleared"}
