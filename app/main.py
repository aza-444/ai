from fastapi import FastAPI
from pydantic import BaseModel

from api.services.ai_agent import chat_with_ai
from app.memory import session_memory

app = FastAPI()


class MessageIn(BaseModel):
    user_id: str
    message: str


@app.post("/chat")
async def chat(msg: MessageIn):
    reply = await chat_with_ai(msg.user_id, msg.message)
    return {"response": reply}


@app.post("/reset")
def reset(msg: MessageIn):
    session_memory.clear(msg.user_id)
    return {"status": "cleared"}
