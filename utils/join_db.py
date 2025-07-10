import json
from pathlib import Path

JOIN_PATH = Path("data/join_requests.json")

def load_join_requests():
    if JOIN_PATH.exists():
        with open(JOIN_PATH, "r") as f:
            return json.load(f)
    return []

def save_join_requests(data):
    with open(JOIN_PATH, "w") as f:
        json.dump(data, f, indent=2)

def add_join_request(user_id, chat_id):
    data = load_join_requests()
    if not any(req["user_id"] == user_id and req["chat_id"] == chat_id for req in data):
        data.append({"user_id": user_id, "chat_id": chat_id})
        save_join_requests(data)

def has_join_request(user_id, chat_id):
    data = load_join_requests()
    return any(req["user_id"] == user_id and req["chat_id"] == chat_id for req in data)
