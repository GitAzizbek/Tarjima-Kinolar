import json
import os
from config import MOVIE_JSON_PATH, USERS_JSON_PATH

CHANNELS_PATH = "data/channels.json"

def load_channels():
    try:
        with open(CHANNELS_PATH, "r") as f:
            return json.load(f)
    except:
        return []

def save_channels(channels):
    with open(CHANNELS_PATH, "w") as f:
        json.dump(channels, f, indent=4)

def add_channel(username):
    channels = load_channels()
    if username not in channels:
        channels.append(username)
        save_channels(channels)

def remove_channel(username):
    channels = load_channels()
    if username in channels:
        channels.remove(username)
        save_channels(channels)


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
