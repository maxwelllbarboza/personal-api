from fastapi import Header, HTTPException, Depends
from .security import decode_token

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Token ausente")
    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_token(token)
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

def require_professor(user = Depends(get_current_user)):
    if user.get("role") != "PROFESSOR":
        raise HTTPException(status_code=403, detail="Acesso restrito a PROFESSOR")
    return user
