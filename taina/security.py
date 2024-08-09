import base64
import hashlib

from .core import config


def verify_password(plain_password: str, hashed_password: str) -> bool:
    new_hash = hash_password(plain_password)
    return new_hash == hashed_password


def hash_password(password: str) -> str:
    password = password.encode("utf-8")
    salt = config.security.user_password_salt.encode("utf-8")
    hashed_password = hashlib.scrypt(password, salt=salt, n=4096, r=8, p=1)
    return base64.b64encode(hashed_password).decode("utf-8")
