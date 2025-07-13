import pytest
import asyncio
from typing import AsyncGenerator


@pytest.mark.asyncio
async def test_generate_reply_stream(monkeypatch):
    # Mock session_memory
    class MockSessionMemory:
        def __init__(self):
            self.data = {}
        def add(self, user_id, role, message):
            self.data.setdefault(user_id, []).append({"role": role, "content": message})
        def get(self, user_id):
            return self.data.get(user_id, [{"role": "user", "content": "salom"}])

    # Mock response chunk
    class MockResponseChunk:
        def __init__(self, content):
            self.choices = [
                type("Choice", (), {
                    "delta": type("DeltaContent", (), {"content": content})()
                })()
            ]

    # Mock stream response (async iterable object)
    class MockStreamResponse:
        def __aiter__(self):
            return self._aiter()

        async def _aiter(self):
            for word in ["Hello", "world"]:
                await asyncio.sleep(0.01)
                yield MockResponseChunk(word)

    # Async function that returns a mock stream response
    async def mock_create(model, messages, temperature, stream):
        return MockStreamResponse()

    # Mock OpenAI client
    class MockClient:
        class chat:
            class completions:
                create = staticmethod(mock_create)

    # Patch the module's session_memory and client
    import api.services.ai_agent as ai_agent
    ai_agent.session_memory = MockSessionMemory()
    ai_agent.client = MockClient()

    # Test actual generator
    user_id = "123"
    user_message = "Test message"
    result = []
    async for res in ai_agent.generate_reply_stream(user_id, user_message):
        result.append(res)

    # Join and assert
    joined = " ".join(result)
    assert "Hello" in joined
    assert "world" in joined
