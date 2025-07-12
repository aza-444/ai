import json
from collections import defaultdict
from datetime import datetime
class SessionMemory:
    def __init__(self):
        self.memory = defaultdict(list)

    def add(self, user_id, role, content):

        self.memory[user_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.memory[user_id] = self.memory[user_id][-8:]

    def get(self, user_id):
        return self.memory[user_id]

    def clear(self, user_id):
        self.memory[user_id] = []

    def save_to_disk(self, filename="session_backup.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)

    def load_from_disk(self, filename="session_backup.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.memory = defaultdict(list, data)
        except FileNotFoundError:
            pass
session_memory = SessionMemory()