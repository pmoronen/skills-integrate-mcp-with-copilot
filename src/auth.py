"""Teacher credential loading and password hashing helpers."""

import hashlib
import json
import secrets
from pathlib import Path

TEACHERS_FILE = Path(__file__).parent / "teachers.json"
PASSWORD_HASH_ITERATIONS = 310_000


class TeacherCredentialsError(RuntimeError):
    """Raised when the local teacher credential file is unavailable or invalid."""


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_HASH_ITERATIONS
    )
    return f"pbkdf2_sha256${PASSWORD_HASH_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, encoded_hash: str) -> bool:
    try:
        algorithm, iterations, salt_hex, digest_hex = encoded_hash.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        salt = bytes.fromhex(salt_hex)
        expected_digest = bytes.fromhex(digest_hex)
        actual_digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, int(iterations)
        )
    except (ValueError, TypeError):
        return False
    return secrets.compare_digest(actual_digest, expected_digest)


def load_teachers() -> dict[str, str]:
    try:
        with TEACHERS_FILE.open(encoding="utf-8") as teachers_file:
            data = json.load(teachers_file)
    except FileNotFoundError as error:
        raise TeacherCredentialsError(
            f"Teacher credentials are missing: create {TEACHERS_FILE} "
            "with `python -m src.create_teacher <username>`"
        ) from error
    except json.JSONDecodeError as error:
        raise TeacherCredentialsError(
            f"Invalid teacher credentials JSON in {TEACHERS_FILE}"
        ) from error

    teachers = data.get("teachers") if isinstance(data, dict) else None
    if not isinstance(teachers, dict) or not all(
        isinstance(username, str) and isinstance(password_hash, str)
        for username, password_hash in teachers.items()
    ):
        raise TeacherCredentialsError(
            f"Invalid teacher credentials format in {TEACHERS_FILE}"
        )
    return teachers
