from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select
from ..db import SessionLocal
from ..models import Pessoa
from ..schemas import PessoaCreate, PessoaOut
from ..security import hash_password
from ..deps import require_professor

router = APIRouter(prefix="/pessoas", tags=["pessoas"])

@router.post("", response_model=PessoaOut, dependencies=[Depends(require_professor)])
def create_pessoa(body: PessoaCreate):
    with SessionLocal() as db:
        exists = db.execute(select(Pessoa).where(Pessoa.email == body.email.lower())).scalar_one_or_none()
        if exists:
            raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

        obj = Pessoa(
            nome=body.nome,
            email=body.email.lower(),
            perfil_acesso=body.perfil_acesso.upper(),
            telefone=body.telefone,
            data_nascimento=body.data_nascimento,
            senha=hash_password(body.senha),
            status=body.status or "ATIVO",
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return PessoaOut(
            id_pessoa=obj.id_pessoa, nome=obj.nome, email=obj.email,
            perfil_acesso=obj.perfil_acesso, telefone=obj.telefone,
            data_nascimento=obj.data_nascimento, status=obj.status
        )

@router.get("", response_model=list[PessoaOut], dependencies=[Depends(require_professor)])
def list_pessoas(q: str = Query("", description="Busca por nome")):
    with SessionLocal() as db:
        rows = db.execute(select(Pessoa).where(Pessoa.nome.ilike(f"%{q}%"))).scalars().all()
        return [
            PessoaOut(
                id_pessoa=r.id_pessoa, nome=r.nome, email=r.email,
                perfil_acesso=r.perfil_acesso, telefone=r.telefone,
                data_nascimento=r.data_nascimento, status=r.status
            ) for r in rows
        ]