import hashlib
import hmac
import secrets
from database import get_connection


def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        200_000,
    ).hex()

    return salt, password_hash


def verify_password(password, salt, expected_hash):
    _, actual_hash = hash_password(password, salt)
    return hmac.compare_digest(actual_hash, expected_hash)


def authenticate(username, password):
    with get_connection() as conn:
        user = conn.execute(
            """SELECT id, username, password_hash, salt, role
            FROM users WHERE username = ?""",
            (username.strip(),),
        ).fetchone()

    if user and verify_password(
        password, user["salt"], user["password_hash"]
    ):
        return {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"],
        }

    return None


def create_user(username, password, role):
    username = username.strip()

    if len(username) < 3:
        raise ValueError("Username must have at least 3 characters.")

    if len(password) < 8:
        raise ValueError("Password must have at least 8 characters.")

    if role not in ("Admin", "Staff"):
        raise ValueError("Invalid role.")

    salt, password_hash = hash_password(password)

    try:
        with get_connection() as conn:
            conn.execute(
                """INSERT INTO users
                (username, password_hash, salt, role)
                VALUES (?, ?, ?, ?)""",
                (username, password_hash, salt, role),
            )
    except Exception as error:
        if "UNIQUE" in str(error).upper():
            raise ValueError("Username already exists.") from error
        raise