def get_username(user) -> str:
    if user.username:
        return f"@{user.username}"
    return f"{user.first_name}"
