import argparse
import json
import os
import secrets
import sys
from getpass import getpass

import streamlit_authenticator as stauth


VALID_ROLES = {"admin", "supervisor", "auditor"}


def parse_user_spec(user_spec):
    """Parse 'username|name|role|password' into a user payload."""
    parts = [part.strip() for part in user_spec.split("|", 3)]
    if len(parts) != 4:
        raise ValueError(
            "Invalid --user format. Use: username|name|role|password"
        )

    username, name, role, password = parts
    if not username or not name or not role or not password:
        raise ValueError("All user fields are required in --user specification.")

    role = role.lower()
    if role not in VALID_ROLES:
        raise ValueError(f"Invalid role '{role}'. Valid roles: {sorted(VALID_ROLES)}")

    return {
        "username": username.lower(),
        "name": name,
        "role": role,
        "password_hash": stauth.Hasher.hash(password),
    }


def prompt_users_interactively():
    users = []
    print("No --user entries provided. Enter users interactively.")
    print("Press Enter on username to finish.")

    while True:
        username = input("Username (email): ").strip().lower()
        if not username:
            break

        name = input("Display name: ").strip()
        role = input("Role (admin/supervisor/auditor): ").strip().lower()
        if role not in VALID_ROLES:
            print(f"Invalid role '{role}'. Try again.")
            continue

        password = getpass("Password (input hidden): ")
        if not password:
            print("Password cannot be empty. Try again.")
            continue

        users.append(
            {
                "username": username,
                "name": name,
                "role": role,
                "password_hash": stauth.Hasher.hash(password),
            }
        )

    return users


def main():
    parser = argparse.ArgumentParser(
        description="Generate auth_config.json with hashed passwords and strong cookie key."
    )
    parser.add_argument(
        "--output",
        default="auth_config.json",
        help="Output auth config path (default: auth_config.json).",
    )
    parser.add_argument(
        "--cookie-name",
        default="qa_audit_platform_session",
        help="Authentication cookie name.",
    )
    parser.add_argument(
        "--cookie-expiry-days",
        type=int,
        default=1,
        help="Cookie expiry in days.",
    )
    parser.add_argument(
        "--user",
        action="append",
        default=[],
        help="User entry in format username|name|role|password. Repeat for multiple users.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output file if it already exists.",
    )

    args = parser.parse_args()

    output_path = os.path.abspath(args.output)
    if os.path.exists(output_path) and not args.force:
        print(f"Refusing to overwrite existing file: {output_path}")
        print("Use --force to overwrite.")
        return 1

    if args.cookie_expiry_days < 1:
        print("--cookie-expiry-days must be at least 1.")
        return 1

    users = []
    try:
        for user_spec in args.user:
            users.append(parse_user_spec(user_spec))
    except Exception as exc:
        print(f"Failed to parse --user: {exc}")
        return 1

    if not users:
        users = prompt_users_interactively()

    if not users:
        print("No users provided. Nothing to write.")
        return 1

    payload = {
        "cookie_name": args.cookie_name,
        "cookie_key": secrets.token_urlsafe(48),
        "cookie_expiry_days": args.cookie_expiry_days,
        "users": users,
    }

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)

    print("Auth config generated successfully.")
    print(f"Path: {output_path}")
    print(f"Users: {len(users)}")
    for user in users:
        print(f"- {user['username']} ({user['role']})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
