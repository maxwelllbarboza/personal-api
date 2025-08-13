import hashlib, jwt
from datetime import datetime, timedelta
from .config import JWT_SECRET, JWT_ALG, JWT_EXPIRES_MIN

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hash_hex: str) -> bool:
    return hash_password(password) == hash_hex

def create_token(sub: str, role: str) -> str:
    exp = datetime.utcnow() + timedelta(minutes=JWT_EXPIRES_MIN)
    payload = {"sub": sub, "role": role, "exp": exp}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
