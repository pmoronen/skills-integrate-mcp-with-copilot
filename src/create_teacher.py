"""Add a teacher account to the local credentials file."""

import getpass
import json
import sys

from src.auth import TEACHERS_FILE, hash_password


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        raise SystemExit("Usage: python -m src.create_teacher <username>")

    username = sys.argv[1].strip()
    password = getpass.getpass("Teacher password: ")
    confirmation = getpass.getpass("Confirm password: ")
    if not password:
        raise SystemExit("Password cannot be empty")
    if password != confirmation:
        raise SystemExit("Passwords do not match")

    if TEACHERS_FILE.exists():
        with TEACHERS_FILE.open(encoding="utf-8") as teachers_file:
            data = json.load(teachers_file)
    else:
        data = {"teachers": {}}

    teachers = data.get("teachers")
    if not isinstance(teachers, dict):
        raise SystemExit(f"Invalid teacher credentials format in {TEACHERS_FILE}")
    if username in teachers:
        raise SystemExit(f"Teacher {username!r} already exists")

    teachers[username] = hash_password(password)
    with TEACHERS_FILE.open("w", encoding="utf-8") as teachers_file:
        json.dump(data, teachers_file, indent=2)
        teachers_file.write("\n")
    print(f"Added teacher {username!r} to {TEACHERS_FILE}")


if __name__ == "__main__":
    main()
