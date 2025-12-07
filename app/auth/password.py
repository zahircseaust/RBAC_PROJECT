import bcrypt
import hashlib


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    # If password is longer than 72 bytes, hash it with SHA-256 first
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        password_bytes = hashlib.sha256(password_bytes).hexdigest().encode("utf-8")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    # Apply same logic for verification
    password_bytes = plain_password.encode("utf-8")
    if len(password_bytes) > 72:
        password_bytes = hashlib.sha256(password_bytes).hexdigest().encode("utf-8")
    try:
        return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))
    except Exception:
        return False
