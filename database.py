import json
import os
from config import MOVIE_JSON_PATH, USERS_JSON_PATH

CHANNELS_PATH = "data/channels.json"

def load_channels():
    """Saqlangan kanallar ro‘yxatini qaytaradi"""
    if not os.path.exists(CHANNELS_PATH):
        return []
    with open(CHANNELS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_channels(channels):
    """Kanallar ro‘yxatini faylga saqlaydi"""
    with open(CHANNELS_PATH, "w", encoding="utf-8") as f:
        json.dump(channels, f, indent=2, ensure_ascii=False)


def add_channel(channel: dict):
    """
    Kanal qo‘shish (public/private) uchun.
    channel: {
        "type": "public" | "private",
        "chat_id": "-100...",
        "url": "https://t.me/+abc123" | "https://t.me/kanal_username",
        "title": "Kanal nomi"
    }
    """
    channels = load_channels()
    if any(ch.get("chat_id") == channel["chat_id"] for ch in channels):
        return False  # Avvaldan mavjud bo‘lsa, qo‘shmaydi

    channels.append(channel)
    save_channels(channels)
    return True

def remove_channel(chat_id: str) -> bool:
    channels = load_channels()
    new_channels = [ch for ch in channels if ch["chat_id"] != chat_id]
    if len(new_channels) == len(channels):
        return False  # hech nima o‘zgarmadi
    save_channels(new_channels)
    return True



# === KINO BILAN ISHLASH ===
def load_movies():
    if not os.path.exists(MOVIE_JSON_PATH):
        with open(MOVIE_JSON_PATH, "w") as f:
            json.dump({}, f)
    with open(MOVIE_JSON_PATH, "r") as f:
        return json.load(f)


def save_movie(code, data):
    code = code.upper()
    movies = load_movies()
    movies[code] = data
    with open(MOVIE_JSON_PATH, "w") as f:
        json.dump(movies, f, indent=4)


def get_movie_by_code(code):
    code = code.upper()
    movies = load_movies()
    return movies.get(code)


# === FOYDALANUVCHILAR BILAN ISHLASH ===
def load_users():
    if not os.path.exists(USERS_JSON_PATH):
        with open(USERS_JSON_PATH, "w") as f:
            json.dump([], f)
    with open(USERS_JSON_PATH, "r") as f:
        return json.load(f)


def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USERS_JSON_PATH, "w") as f:
            json.dump(users, f, indent=4)


def get_user_count():
    return len(load_users())

def save_user(user):
    users = load_users()

    user_data = {
        "id": user.id,
        "first_name": user.first_name or "",
        "last_name": user.last_name or "",
        "username": user.username or ""
    }

    # Takror bo'lmasin
    if not any(u["id"] == user.id for u in users):
        users.append(user_data)
        with open(USERS_JSON_PATH, "w") as f:
            json.dump(users, f, indent=4)
