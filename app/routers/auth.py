from fastapi import APIRouter, HTTPException
from sqlalchemy import select, update
from datetime import datetime, timedelta
from ..db import SessionLocal
from ..models import Pessoa
from ..schemas import LoginIn, TokenOut
from ..security import verify_password, create_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenOut)
def login(data: LoginIn):
    with SessionLocal() as db:
        user = db.execute(select(Pessoa).where(Pessoa.email == data.email.lower())).scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário ou senha incorreto.")

        if user.status == "INATIVO" and user.data_hora_bloqueio:
            if datetime.utcnow() < user.data_hora_bloqueio + timedelta(minutes=30):
                raise HTTPException(status_code=403, detail="Usuário bloqueado. Tente novamente mais tarde.")
            db.execute(update(Pessoa).where(Pessoa.email == user.email).values(status="ATIVO", tentativas=0, data_hora_bloqueio=None))
            db.commit()

        if not verify_password(data.senha, user.senha):
            tent = (user.tentativas or 0) + 1
            vals = {"tentativas": tent}
            if tent >= 3:
                vals["status"] = "INATIVO"
                vals["data_hora_bloqueio"] = datetime.utcnow()
            db.execute(update(Pessoa).where(Pessoa.email == user.email).values(**vals))
            db.commit()
            raise HTTPException(status_code=401, detail="Usuário ou senha incorreto.")

        db.execute(update(Pessoa).where(Pessoa.email == user.email).values(tentativas=0, status="ATIVO", data_hora_bloqueio=None))
        db.commit()

        token = create_token(str(user.id_pessoa), user.perfil_acesso)
        return TokenOut(access_token=token)