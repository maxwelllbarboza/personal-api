from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date
import uuid

class LoginIn(BaseModel):
    email: EmailStr
    senha: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PessoaBase(BaseModel):
    nome: str
    email: EmailStr
    perfil_acesso: str
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    status: Optional[str] = "ATIVO"

class PessoaCreate(PessoaBase):
    senha: str

class PessoaOut(BaseModel):
    id_pessoa: uuid.UUID
    nome: str
    email: EmailStr
    perfil_acesso: str
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    status: str

class ExerciseCreate(BaseModel):
    category: str
    name: str
    image: Optional[str] = None

class ExerciseOut(BaseModel):
    id: int
    category: str
    name: str
    image: Optional[str] = None

class WorkoutCreate(BaseModel):
    student_email: EmailStr
    workout_name: str
    exercise_ids: Optional[List[int]] = None

class WorkoutOut(BaseModel):
    id: uuid.UUID
    student_email: EmailStr
    workout_name: str
    creation_date: date
    exercise_ids: Optional[str] = None
    status: str