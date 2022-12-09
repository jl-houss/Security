import secrets
from base64 import urlsafe_b64decode as b64d
from base64 import urlsafe_b64encode as b64e

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def center(w, h, frame):
    ws = frame.winfo_screenwidth()
    hs = frame.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    frame.geometry("%dx%d+%d+%d" % (w, h, x, y))
    clear(frame)


def _derive_key(password: bytes, salt: bytes, iterations: int = 100_000) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend(),
    )
    return b64e(kdf.derive(password))


def password_encrypt(message: str, password: str, iterations: int = 100_000) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    encrypted = b64e(
        b"%b%b%b"
        % (
            salt,
            iterations.to_bytes(4, "big"),
            b64d(Fernet(key).encrypt(message.encode())),
        )
    )
    return encrypted.decode()


def password_decrypt(token: str, password: str) -> bytes:
    decoded = b64d(token.encode())
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, "big")
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token).decode()
