import json
import os


def _load_users_from_payload(payload):
    users = payload.get("users", [])
    if not users:
        raise ValueError("No users found in auth config.")

    credentials = {"usernames": {}}
    role_map = {}

    for user in users:
        username = str(user.get("username", "")).strip().lower()
        name = str(user.get("name", "")).strip()
        password_hash = str(user.get("password_hash", "")).strip()
        role = str(user.get("role", "")).strip().lower()

        if not username or not name or not password_hash or not role:
            raise ValueError("Each user must include username, name, password_hash, and role.")

        credentials["usernames"][username] = {
            "name": name,
            "password": password_hash,
        }
        role_map[username] = role

    return credentials, role_map


def load_auth_settings(base_dir):
    """
    Load auth settings from either:
    1) QA_AUTH_CONFIG_PATH (JSON file path), or
    2) auth_config.json in the repository root.
    """
    configured_path = os.getenv("QA_AUTH_CONFIG_PATH", "").strip()
    config_path = configured_path or os.path.join(base_dir, "auth_config.json")

    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Auth config file not found at: {config_path}. "
            "Set QA_AUTH_CONFIG_PATH or create auth_config.json from auth_config.example.json."
        )

    with open(config_path, "r", encoding="utf-8") as file:
        payload = json.load(file)

    credentials, role_map = _load_users_from_payload(payload)

    cookie_name = str(payload.get("cookie_name", "")).strip()
    cookie_key = str(payload.get("cookie_key", "")).strip()
    cookie_expiry_days = int(payload.get("cookie_expiry_days", 1))

    if not cookie_name or not cookie_key:
        raise ValueError("cookie_name and cookie_key are required in auth config.")

    return {
        "credentials": credentials,
        "role_map": role_map,
        "cookie_name": cookie_name,
        "cookie_key": cookie_key,
        "cookie_expiry_days": cookie_expiry_days,
        "config_path": config_path,
    }
