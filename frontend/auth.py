from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / ".travel_advisor_data"
USERS_FILE = DATA_DIR / "users.json"

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PBKDF2_ITERATIONS = 200_000
SALT_BYTES = 16


def _load_users() -> dict[str, dict]:
    if not USERS_FILE.exists():
        return {}
    try:
        data = json.loads(USERS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def _save_users(users: dict[str, dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    USERS_FILE.write_text(
        json.dumps(users, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _hash_password(password: str, salt: bytes) -> str:
    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return derived.hex()


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))


def validate_password(password: str) -> str | None:
    if len(password) < 8:
        return "Mật khẩu phải có ít nhất 8 ký tự."
    if not re.search(r"[A-Za-z]", password):
        return "Mật khẩu phải có ít nhất 1 chữ cái."
    if not re.search(r"\d", password):
        return "Mật khẩu phải có ít nhất 1 chữ số."
    return None


def register_user(email: str, password: str, confirm_password: str) -> tuple[bool, str]:
    email = email.strip().lower()

    if not email:
        return False, "Vui lòng nhập email."
    if not is_valid_email(email):
        return False, "Email không đúng định dạng."
    if password != confirm_password:
        return False, "Mật khẩu nhập lại không khớp."

    pwd_error = validate_password(password)
    if pwd_error:
        return False, pwd_error

    users = _load_users()
    if email in users:
        return False, "Email đã được đăng ký."

    salt = secrets.token_bytes(SALT_BYTES)
    users[email] = {
        "email": email,
        "salt": salt.hex(),
        "password_hash": _hash_password(password, salt),
        "iterations": PBKDF2_ITERATIONS,
        "created_at": datetime.utcnow().isoformat(),
    }
    _save_users(users)
    return True, "Đăng ký thành công. Vui lòng đăng nhập."


def authenticate(email: str, password: str) -> tuple[bool, str]:
    email = email.strip().lower()

    if not email or not password:
        return False, "Vui lòng nhập email và mật khẩu."

    users = _load_users()
    user = users.get(email)
    if not user:
        return False, "Email hoặc mật khẩu không đúng."

    try:
        salt = bytes.fromhex(user["salt"])
        expected = user["password_hash"]
    except (KeyError, ValueError):
        return False, "Dữ liệu tài khoản không hợp lệ."

    actual = _hash_password(password, salt)
    if not secrets.compare_digest(actual, expected):
        return False, "Email hoặc mật khẩu không đúng."

    return True, "Đăng nhập thành công."
