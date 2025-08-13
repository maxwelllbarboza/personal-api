from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, Date, Integer, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Base(DeclarativeBase):
    pass

class Pessoa(Base):
    __tablename__ = "pessoa"
    id_pessoa: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    data_nascimento: Mapped[str | None] = mapped_column(Date, nullable=True)
    telefone: Mapped[str | None] = mapped_column(Text, nullable=True)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    perfil_acesso: Mapped[str] = mapped_column(String(20), nullable=False)  # 'PROFESSOR' | 'ALUNO'
    status: Mapped[str] = mapped_column(String(10), default="ATIVO")
    senha: Mapped[str] = mapped_column(Text, nullable=False)                # hash
    data_hora_bloqueio: Mapped[str | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    tentativas: Mapped[int] = mapped_column(Integer, default=0)

class Exercise(Base):
    __tablename__ = "exercises"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str | None] = mapped_column(Text, nullable=True)

class Workout(Base):
    __tablename__ = "workouts"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_email: Mapped[str] = mapped_column(Text, nullable=False)  # referencia Pessoa.email
    workout_name: Mapped[str] = mapped_column(Text, nullable=False)
    creation_date: Mapped[str] = mapped_column(Date, nullable=False, server_default=func.current_date())
    exercise_ids: Mapped[str | None] = mapped_column(Text, nullable=True)  # "1,5,7"
    status: Mapped[str] = mapped_column(String(12), default="ATIVO")       # ATIVO | EXPIRADO | CANCELADO
