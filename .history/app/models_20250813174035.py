from sqlalchemy import Column, String, Integer, DateTime, Text
from .db import Base
import uuid
from datetime import datetime

class Pessoa(Base):
    __tablename__ = "pessoa"
    id_pessoa = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String, nullable=False)
    data_nascimento = Column(String)
    telefone = Column(String)
    email = Column(String, unique=True, nullable=False)
    perfil_acesso = Column(String, nullable=False)
    status = Column(String, default="ATIVO")
    senha = Column(String, nullable=False)
    data_hora_bloqueio = Column(DateTime, nullable=True)
    tentativas = Column(Integer, default=0)

class Workout(Base):
    __tablename__ = "workouts"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_email = Column(String, nullable=False)
    workout_name = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow)
    exercise_ids = Column(Text)
    status = Column(String, default="ATIVO")
