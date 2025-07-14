from fastapi import FastAPI, Request
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from api.services.ai_agent import generate_reply_stream
from app.memory import session_memory

app = FastAPI()


class MessageIn(BaseModel):
    user_id: str
    message: str


@app.post("/chat-stream")
async def chat_stream(msg: MessageIn):
    return StreamingResponse(
        generate_reply_stream(msg.user_id, msg.message), media_type="text/plain"
    )

@app.post("/reset")
def reset(msg: MessageIn):
    session_memory.clear(msg.user_id)
    return {"status": "cleared"}
