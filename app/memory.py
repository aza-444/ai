from collections import defaultdict

class SessionMemory:
    def __init__(self):
        self.memory = defaultdict(list)

    def add(self, user_id, role, content):
        self.memory[user_id].append({"role": role, "content": content})
        self.memory[user_id] = self.memory[user_id][-10:]

    def get(self, user_id):
        return self.memory[user_id]

    def clear(self, user_id):
        self.memory[user_id] = []

session_memory = SessionMemory()
