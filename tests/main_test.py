import pytest

@pytest.mark.asyncio
async def test_generate_reply_stream(monkeypatch):
    class MockSessionMemory:
        def __init__(self):
            self.data = {}
        def add(self, user_id, role, message):
            self.data.setdefault(user_id, []).append({"role": role, "content": message})
        def get(self, user_id):
            return self.data.get(user_id, [{"role": "user", "content": "salom"}])

    class MockResponseChunk:
        def __init__(self, content):
            self.choices = [type("Delta", (), {"delta": type("DeltaContent", (), {"content": content})})()]

    class MockClient:
        class chat:
            class completions:
                @staticmethod
                async def create(model, messages, temperature, stream):
                    for text in ["Hello", "world"]:
                        yield MockResponseChunk(text)

    import api.services.ai_agent as ai_agent
    ai_agent.session_memory = MockSessionMemory()
    ai_agent.client = MockClient()

    user_id = "123"
    user_message = "Test message"
    result = []
    async for res in ai_agent.generate_reply_stream(user_id, user_message):
        result.append(res)
    assert "Hello" in " ".join(result)
    assert "world" in " ".join(result)